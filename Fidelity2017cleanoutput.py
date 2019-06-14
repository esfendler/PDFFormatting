

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

street_indicators = ["ARBORWAY", "ACCOUNTING", "ADMINISTRATION", "ADMIN", "BROADMEAD", "DOVECREEK", "WOLFLIN",
                     "ARBORETUM", "Broadway", "BROADWAY", "OFFICE", "department", "Dept", "DEPARTMENT", "Court",
                     "Crescent", "Circle", "Road", "street", "floor", "FLOOR", "rd", "st", "Ln", "LANE", "drive",
                     "STREET", "place", "ROAD", "ST", "NW", "Nw", "NE", "Ne", "SE", "SW", "Terrace", "Street", "avenue",
                     "TPKE", "Floor", "Plaza", "Pkwy", "Pky", "SPEEDWAY", "Place", "AVENUE", "Dr", "Lane", "St", "CT",
                     "station", "sta", "Blvd", "blvd", "BLVD", "Boulevard", "boulevard", "BOULEVARD", "Avenue", "Drive",
                     "DRIVE", "Rd", "PL", "DR", "square", "Ct", "Trail", "Rd.", "Ave", "AVE", "ave", "RD", "SQ", "Sq",
                     "LN", "WAY", "Way", "Highway", "HWY", "EXPRESSWAY", "HIGHWAY", "Parkway", "PKWY", "TER", "PIKE",
                     "Pike", "Hwy", "MEADOWCREEK", "TNRB", "SWKT", "ORNAC", "ELGIN", "FENWAY","STA", "TRL", "FL", "STE","LOOP", "CIR", "PLACE", "PLZ", "CTR", "FLR", "AV", "PKY", "PARKWAY", "EXPY", "PLAZA"]

address_indicators = ["po", "PO","p.o.", "p.o.b.","pob","POB","box","cpo", "p.o.box", "p.o","PMB","pmb","fenno", "p.", "BOX"]

input_file = r"C:\\Users\esf\Desktop\Fidelity 2017 Development\Final Input Files\Fidelity2017_FinalInput_pt1.txt"
output_file = r"C:\\Users\esf\Desktop\Fidelity 2017 Development\Test Outputs\Fidelity 2017 Test Output.txt"

records = []
prior_lines = []

with open(input_file) as in_file:
    field_string = ""
    counter = 0
    for line in in_file.readlines():

        counter += 1
        if counter % 1000 == 0:
            print("Processed {} lines".format(counter))
        line = line.strip()
        linefields = line.split(" ")
        linefields = list(filter(None, linefields))
        if linefields[len(linefields) - 1] != "RECIPIENT'":
            beforefiveoh = []
            afterfiveoh = []
            for i, field in list(enumerate(linefields)):
                # line type 1
                fiveohposition = linefields.index("501(C)(3)")
                if i < fiveohposition:
                    beforefiveoh.append(field)
                elif i > fiveohposition:
                    afterfiveoh.append(field)
            amount = afterfiveoh[0].strip(".")
            EIN = beforefiveoh[len(beforefiveoh) - 1]
            if len(EIN) < 10:
                EIN = ""
            recipient = ' '.join(beforefiveoh[1:len(beforefiveoh) - 1])
            if EIN == "":
                recipient = ' '.join(beforefiveoh[1:len(beforefiveoh)])
            address = ' '.join(afterfiveoh[6:len(afterfiveoh)])
            PossibleZip = afterfiveoh[len(afterfiveoh) - 1]
            if PossibleZip.isdigit and len(PossibleZip) == 5:
                Zip = ''
                Zip = PossibleZip
                address = ' '.join(afterfiveoh[6:len(afterfiveoh)-1])

            address_split = address.split()
            possible_state = address_split[len(address_split) - 1]
            state_finder = [a in possible_state for a in states]
            state = ''
            if True in state_finder:
                state = possible_state
                city = ''
                addresslen = len(address_split)
                c = address_split[addresslen - 3]
                cChar = list(c)
                address = ' '.join(address_split[0:len(address_split) - 2])
                if c in street_indicators or c.isdigit():
                    # If that's the end of an address we have a one-word city
                    city = address_split[addresslen - 2]
                    city = city.replace(",", "")
                    address = ' '.join(address_split[0:len(address_split) - 2])
                elif any(z == "." for z in cChar):
                    city = address[addresslen - 1]
                    city = city.replace(",", "")
                    address = address[0:addresslen - 1]
                elif any(z.islower() for z in cChar):
                    city = address[addresslen - 1]
                    city = city.replace(",", "")
                    address = address[0:addresslen - 1]
                elif any(z.isdigit() for z in cChar):
                    city = address[addresslen - 1]
                    city = city.replace(",", "")
                    address = address[0:addresslen - 1]
                elif len(cChar) == 1:
                    try:
                        city = address_split[addresslen - 2]
                        city = city.replace(",", "")
                    except:
                        if addresslen < 1:
                            city = "WHAT"

                else:
                    # Otherwise, assume a two-word city
                    city = " ".join(address_split[addresslen - 3:addresslen-1])
                    city = city.replace(",", "")
                    address = " ".join(address_split[0:addresslen - 3])
            else:
                city = ''
                Zip = ''
                state = ''

            parsed_line = "\t".join([EIN, amount, recipient, address, city, state, Zip,line])
            city = ''
            state = ''
            Zip = ''
        else:  # line type 2
            amount = linefields[len(linefields) - 6]
            amount = amount.replace(".", "")
            EIN = linefields[len(linefields) - 8]
            zip = linefields[len(linefields) - 9]
            state = linefields[len(linefields) - 10]
            state_finder = [l in state for l in states]


            city = ''
            recipientstreetcity = linefields[1:len(linefields) - 10]

            addresscount = len(recipientstreetcity)
            c = recipientstreetcity[addresscount - 2]
            cChar = list(c)
            remaining = ' '.join(recipientstreetcity[0:addresscount - 2])
            if c in street_indicators or c.isdigit():
                # If that's the end of an address we have a one-word city
                city = recipientstreetcity[addresscount - 1]
                city = city.replace(",", "")
                remaining = ' '.join(recipientstreetcity[0:len(recipientstreetcity) - 1])
            elif any(z == "." for z in cChar):
                city = recipientstreetcity[addresscount - 1]
                city = city.replace(",", "")
                remaining = ' '.join(recipientstreetcity[0:len(recipientstreetcity) - 1])
            elif any(z.islower() for z in cChar):
                city = recipientstreetcity[addresscount - 1]
                city = city.replace(",", "")
                remaining = ' '.join(recipientstreetcity[0:len(recipientstreetcity) - 1])
            elif any(z.isdigit() for z in cChar):
                city = recipientstreetcity[addresscount - 1]
                city = city.replace(",", "")
                remaining = ' '.join(recipientstreetcity[0:len(recipientstreetcity) - 1])
            elif len(cChar) == 1:
                try:
                    city = recipientstreetcity[addresscount - 1]
                    city = city.replace(",", "")
                    remaining = ' '.join(recipientstreetcity[0:len(recipientstreetcity) - 1])
                except:
                    if addresscount < 1:
                        city = "WHAT"
            else:
                # Otherwise, assume a two-word city
                city = " ".join(recipientstreetcity[addresscount - 2:addresscount])
                city = city.replace(",", "")
                remaining = " ".join(recipientstreetcity[0:addresscount - 2])

            remaining = list(remaining.split(" "))
            address = ""

            address_starter = ""
            name = ""
            for i in range(1,len(remaining)):
                # Look at the remaining words and if any indicate the start of an address, split on that word:
                if remaining[i] in address_indicators and name == "":
                    name = str(" ".join(remaining[:i]))
                    address = str(" ".join(remaining[i:]))
                    address_starter = remaining[i]
                elif remaining[i].isdigit()and address_starter == "":
                    name = str(" ".join(remaining[:i]))
                    address = str(" ".join(remaining[i:]))
                    address_starter = remaining[i]
                elif not remaining[i].isdigit()and not remaining[i].isalpha() and address_starter == "":
                    name = str(" ".join(remaining[:i]))
                    address = str(" ".join(remaining[i:]))
                    address_starter = remaining[i]
            if address_starter == "":
                name = str(" ".join(remaining))
                address = ""


            parsed_line = "\t".join([EIN, amount, name, address,city, state, zip,line, "!!!"])
            city = ''
            state = ''
            Zip = ''
        with open(output_file, "a") as out_file:
            out_file.write(parsed_line + "\n")




