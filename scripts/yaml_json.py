import yaml

stream = open('../gsapi/data/collections/typs.yaml', 'r')
y = yaml.load(stream)
print y

