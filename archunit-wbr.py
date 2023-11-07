import csv
import sys

headers = []
services = set()
archunit = {}
archunit_filtered = {}
archunit_violations = {}

# Hardcoded list of required rules - check the compliance dashboard manually to see if this list is correct
required_rules = {'noRouxSpringConfigDeprecated', 'noRouxApiTestDeprecated', 'noJodaTimeConfig', 'noRouxSpringFigDeprecated', 'serviceVisibilityForRouteSpecImpl', 'serviceVisibilityForRouteSpecNoInterface', 'noRouxTestDeprecated', 'noDeprecatedMockito', 'serviceVisibilityForRouteSpecNoImpl', 'noCasseroleDeprecated'}

def load_input(services_filename, archunit_filename):
    """"Load the service and archunit CSV inputs files
    """
    global headers

    with open(services_filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            services.add(row[0])

    with open(archunit_filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = ['service'] + next(reader)[1:]
        for row in reader:
            archunit[row[0]] = {key: str(value) for key, value in zip(headers, row[0:])}

def filter_archunit():
    """Filter the archunit dictionary to the services listed in the input services CSV
    """
    for service, details in archunit.items():
        # service is a string in the format: <service naem>:<service version>
        service_name = service.split(":")[0]
        if service_name in services and service_name:
            archunit_filtered[service] = details

def filter_violations():
    """Filter the archunit dictionary of the services we are interested in to only the rules that are not in
    compliance.
    """
    for service, details in archunit_filtered.items():
        violations = []
        for unit, compliant in details.items():
            if compliant == 'FALSE' and unit in required_rules:
                violations = violations + [unit]
        archunit_violations[service] = violations

# def write_output():
#     with open('temp.csv', 'w') as output:
#         dw = csv.DictWriter(output, delimiter=',', fieldnames=headers)
#         dw.writeheader()
#         for service,row in archunit_filtered.items():
#             dw.writerow(row)

def write_output(output_csv_filename):
    """Output the final report CSV
    """
    with open(output_csv_filename, 'w') as output:
        w = csv.writer(output, delimiter=',')
        w.writerow(['Service', 'Archunit rules out of compliance'])
        for service, violations in archunit_violations.items():
            w.writerow([service, ','.join(violations)])

if __name__ == '__main__':
    #load_input(sys.argv[1], sys.argv[2])
    services_csv_filename = "services.csv"
    archunit_csv_filename = "archunit.csv"
    output_csv_filename = "temp.csv"
    print(f"Loading service CSV {services_csv_filename} and archunit CSV {archunit_csv_filename}")
    load_input(services_csv_filename, archunit_csv_filename)
    filter_archunit()
    filter_violations()

    print(f"Writing output result to {output_csv_filename}")
    write_output(output_csv_filename)
