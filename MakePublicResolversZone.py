#!/usr/bin/env python3
import json, socket, pprint, base64

''' Program to read a JSON file with information about public resolvers and write out a file to be included with a zone '''

# This program is still very much a work in progress. Features to add are:
#    Command-line options to override the file names and the prepend name
#    Testing using dnspython

# The public resolvers list, as a JSON object
in_file_name = "PublicResolversData.json"
# The output file
out_file_name = "public-resolvers.include"
# String to prepend to the names of the records in the zone
prepend_string = "pubdns"

# Split a text string of arbitrary length into double-quote delimited strings of 63 characters or shorter
def split_into_char_strings(in_text_string):
	if '"' in in_text_string:
		exit("Found a \" in the input string {}. Exiting.".format(in_text_string))
	in_copy = in_text_string
	# List of shorter strings
	out_strings = []
	while len(in_copy) > 63:
		out_strings.append(in_copy[0:62])
		in_copy = in_copy[62:]
	# Be sure to include the last chunk
	if len(in_copy) > 0:
		out_strings.append(in_copy)
	# Add the quotation marks and join them together with spaces
	return " ".join([ '"' + x + '"' for x in out_strings ])

# Read the data
try:
	file_contents = open(in_file_name, mode="r").read()
except Exception as this_e:
	exit("Could not read {}: {}. Exiting.".format(in_file_name, this_e))
try:
	data_in = json.loads(file_contents)
except Exception as e:
	exit("Input data file was not valid JSON: {}. Exiting.".format(e))

# Start the output file
try:
	out_f = open(out_file_name, mode="w")
except Exception as this_e:
	exit("Could not write to {}: {}. Exiting.".format(out_file_name, this_e))

# Counter for the oputput records
counter = 0

for this_resolver in sorted(data_in):
	counter += 1
	if counter > 99:
		exit("There are more than 99 public resolvers but this program uses formatting for two digits. Exiting.")
	out_f.write('{}{:02} IN TXT "{}"\n'.format(prepend_string, counter, this_resolver))
	# Include a TXT record of the JSON of this input record
	pretty_record = pprint.pformat(data_in[this_resolver], width=10000, indent=0)
	character_strings_of_record = split_into_char_strings(pretty_record)
	out_f.write('{}{:02} IN TXT {}\n'.format(prepend_string, counter, character_strings_of_record))
	# Find the addresses for A and AAAA records
	for this_addr in (data_in[this_resolver]).get("addresses", []):
		try:
			this_out_addr = socket.inet_pton(socket.AF_INET6, this_addr)
			out_f.write('{}{:02} IN AAAA {}\n'.format(prepend_string, counter, this_addr))
		except OSError:
			try:
				this_out_addr = socket.inet_pton(socket.AF_INET, this_addr)
				out_f.write('{}{:02} IN A {}\n'.format(prepend_string, counter, this_addr))
			except OSError:
				exit("Found a bad address in '{}'. Exiting.".format(data_in[this_resolver]))	

# Write out the record that gives the highest value of the counter
out_f.write('{} IN TXT "{:02}"\n'.format(prepend_string, counter))
# Write out the original data as base64
json_as_bytes = bytes(json.dumps(data_in), encoding="utf-8")
json_as_base64_as_text = (base64.standard_b64encode(json_as_bytes)).decode("utf-8")
out_b64 = split_into_char_strings(json_as_base64_as_text)
out_f.write('{} IN TXT {}\n'.format(prepend_string, out_b64))

out_f.close()
print("Finished writing {}".format(out_file_name))
