

input_file = r"C:\\Users\esf\Desktop\Fidelity 2017 Development\Final Input Files\Input PrePython\Schedule-I-990_2017_Pt1.txt"
output_file = r"C:\\Users\esf\Desktop\Fidelity 2017 Development\Final Input Files\Fidelity2017_FinalInput_pt1.txt"
records = []
prior_lines = []
header_indicators = ["SCHEDULE I", "Department of the Treasury", "Name of the organization",
                     "Grants and Other Assistance", "À¾µº", "Complete if the organization", "Open to Public",
                     "Information about Schedule I", "Employer identification number",
                     "FIDELITY INVESTMENTS CHARITABLE GIFT FUND", "11-0303001",
                     "General Information on Grants and Assistance", "Does the organization maintain records", "mmm",
                     "the selection criteria used", "Describe in Part IV",
                     "1 (a) Name and address of organization or government", "Enter total number of section",
                     "3 Enter total number of other organizations listed in the line 1 table",
                     "For Paperwork Reduction Act Notice", "JSA 6E1288 1.000", "8923JK 7377 V 16-7.17"]

grant_starters = ["(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)", "(10)", "(11)", "(12)"]

with open(input_file) as in_file:
    field_string = ""
    counter = 0
    for line in in_file.readlines():

        counter += 1
        if counter % 1000 == 0:
            print("Processed {} lines".format(counter))
        line = line.strip()
        if len(line) < 5:
            continue

        if line == "Inspection":
            continue

        headers_found = [s in line for s in header_indicators]
        if True in headers_found:
            continue

        if len(prior_lines) == 0:
            prior_lines.append(line)
        else:
            previous_line = prior_lines[len(prior_lines) - 1]

            linefields = line.split(" ")
            line_beginner = linefields[0]
            grant_starters_found = [n in line_beginner for n in grant_starters]
            prior_lines.append(line)
            if not True in grant_starters_found:
                second_line_address = line
                combined_line = previous_line + " " + second_line_address
                records = records[:-1]
                records.append(combined_line)
            else:
                records.append(line)

with open(output_file, "a") as out_file:
    for record in records:
        record_fields = record.split()

        out_file.write('%s\n' % record)