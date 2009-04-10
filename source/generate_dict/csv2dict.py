# csv2dict.py
"""Reformat a dicom dictionary csv file (from e.g. standards docs) to Python syntax

   Write the DICOM dictionary elements as:
   tag: (VR, VM, description, isRetired)
   in python format
   
   Also write the repeating groups or elements (e.g. group "50xx")
   as masks that can be tested later for tag lookups that didn't work
"""
#
# Copyright 2008, Darcy Mason
# This file is part of pydicom.
# See the license.txt file

csv_filename = "DICOM_dictionary_2008.csv"
pydict_filename = "_dicom_dict.py"
main_dict_name = "DicomDictionary"
mask_dict_name = "RepeatersDictionary"

def write_dict(f, dict_name, attributes, tagIsString):
    if tagIsString:
        entry_format = """'%s': ('%s', '%s', "%s", '%s')"""
    else:
        entry_format = """%s: ('%s', '%s', "%s", '%s')"""
    f.write("\n%s = {\n" % dict_name)
    f.write(",\n".join(entry_format % attribute for attribute in attributes))
    f.write("}\n")

if __name__ == "__main__":
    import csv  # comma-separated value module, python >=2.3

    csv_reader = csv.reader(file(csv_filename, 'rb'))

    main_attributes = []
    mask_attributes = []
    for row in csv_reader:
        tag, description, VR, VM, isRetired  = row
        tag = tag.strip()   # at least one item has extra blank on end
        group, elem = tag[1:-1].split(",")
        
        # Handle one case "(0020,3100 to 31FF)" by converting to mask
        # Do in general way in case others like this come in future standards
        if " to " in elem:
            from_elem, to_elem = elem.split(" to ")
            if from_elem.endswith("00") and to_elem.endswith("FF"):
                elem = from_elem[:2] + "xx"
            else:
                raise NotImplementedError, "Cannot mask '%s'" % elem
        
        description = description.replace("\x92", "'") # non-ascii apostrophe used 
        description = description.replace("\x96", "-") # non-ascii dash used
		
        # If blank (e.g. (0018,9445) and (0028,0020)), then add dummy vals
        if VR == '' and VM == '' and isRetired:
            VR = 'OB'
            VM = '1'
            description = "Retired-blank"
        
        # Handle retired "repeating group" tags e.g. group "50xx"
        if "x" in group or "x" in elem:
            tag = group + elem # simple concatenation
            mask_attributes.append((tag, VR, VM, description, isRetired))
        else:
            tag = "0x%s%s" % (group, elem)
            main_attributes.append((tag, VR, VM, description, isRetired))

    py_file = file(pydict_filename, "wb")
    py_file.write("# %s\n" % pydict_filename)
    py_file.write('"""DICOM data dictionary auto-generated by %s"""\n' % __file__)
    write_dict(py_file, main_dict_name, main_attributes, tagIsString=False)
    write_dict(py_file, mask_dict_name, mask_attributes, tagIsString=True)

    py_file.close()

    print "Finished creating python file %s containing the dicom dictionary" % pydict_filename
    print "Wrote %d tags" % (len(main_attributes)+len(mask_attributes))
