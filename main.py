import xml.etree.ElementTree as ET
import csv


def xml_to_csv(main_file,*args,output_file="extra_products.csv"):
    rows = []

    # Shopitems ids to prevent duplicity and comparing data
    ids = []
    variant_ids = []

    # Parsing ids from in1.xml, in2.xml
    for xmlfile in args:
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        shopitems = root.findall("./")
        for shopitem in shopitems:

            # Product with multiple variants
            if shopitem.find("./VARIANTS/VARIANT"):
                variants = shopitem.findall("./VARIANTS/")
                for variant in variants:
                    
                    # to prevent duplicity 
                    if variant.attrib["id"] not in variant_ids:
                        variant_ids.append(variant.attrib["id"])
                        
            # Product with single variant
            else:
                if shopitem.attrib["id"] not in ids:
                    ids.append(shopitem.attrib["id"])
                    
    # Comparing obtained ids with ids from in-main.xml
    tree = ET.parse(main_file)
    root = tree.getroot()
    shopitems = root.findall("./")
    for shopitem in shopitems:
        row = []  
    
        # More variants
        if shopitem.find("./VARIANTS/VARIANT"):
            variants = shopitem.findall("./VARIANTS/")
            codes = []
            for variant in variants:
                
                # checking for missing variants
                if variant.attrib["id"] not in variant_ids:
                    code = variant.find("./CODE")
                    codes.append(code.text)
                    
            if codes:
                name=shopitem.find("./NAME")
                row.append(name.text)
                row.append(codes)
                rows.append(row)
                
        # Single variant
        else:
            if shopitem.attrib["id"] not in ids:

                 # looking for a name
                name = shopitem.find("./NAME")
                row.append(name.text)
                
                # looking for a code
                code = shopitem.find("./CODE")
                row.append(code.text)
        
                rows.append(row)    

    # Writing the obtained data into a csv file
    with open(output_file, "w", newline="") as csv_file:
        
        # Header
        fieldnames = ["name", "code"]
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, quotechar="", quoting=csv.QUOTE_NONE)
        csv_writer.writeheader()
        
        for name, codes in rows:

            # For single code
            if type(codes) is not list:
                csv_writer.writerow({"name": name, "code": codes})

            # For multiple codes
            else:
                for code in codes:
                    csv_writer.writerow({"name": name,
                                         "code": code})

xml_to_csv("in-main.xml", "in1.xml", "in2.xml")