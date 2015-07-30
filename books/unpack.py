import os, shutil, subprocess, xml.etree.ElementTree as ET, uuid, sys, json
# -*- coding: UTF-8 -*-

DEBUG = False


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'geroi_nashego_vremeni.epub'
    path = str(uuid.uuid4())
    os.mkdir(path)

    try:
        process(['unzip', filename, '-d' + path])
        content = find_content(path + '/META-INF/container.xml')
        metadata_request = path + '/' + content
        step_one = metadata_list(metadata_request)
        step_two = year_and_id_clean(step_one, path)
        metadata = elem_constr(step_two)
        result = output(metadata)
        out = open('testbook.json', 'w')
        try:
            out.write(json.dumps(result, indent=4, ensure_ascii=False, sort_keys=True).encode('utf-8'))
        finally:
            out.close()
    finally:
        if not DEBUG:
            if os.path.isdir(path):
                shutil.rmtree(path)


def metadata_list(path):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    result = {}
    for child in root:
        if 'metadata' in child.tag:
            metadata = child

    namespace = '{http://purl.org/dc/elements/1.1/}'
    tags = ['title', 'language', 'identifier', 'date', 'creator']
    for elem in metadata.iter():
        for tag in tags:
            if namespace + tag == elem.tag:
                if tag in result:
                    result[tag].append(elem.text)
                else:
                    result[tag] = [elem.text]
    return result


def year_and_id_clean(result, unique):
    if len(result['identifier']) > 1:
        for value in result['identifier']:
            if 'uuid' in value:
                result['identifier'] = [unique]
                break
    else:
        result['identifier'] = [unique]
    year = []
    for item in result['date']:
        year.append(int(item))
    result['year'] = year
    del result['date']
    return result


def elem_constr(result):
    elements = []
    for key in result:
        if key == 'title':
            while len(result[key]) > 1:
                if len(result[key][0]) > len(result[key][1]):
                    del result[key][1]
                else:
                    del result[key][0]
        for value in result[key]:
            element = ET.Element(key)
            element.text = value
            if key == 'creator':
                new_element = creator_clean(element)
                element = new_element
            if key == 'identifier':
                continue
            elements.append(element)
    return elements


def creator_clean(element):
    words = element.text.split(' ')
    word = words[-1]
    result = ET.Element('creator')
    display = ET.SubElement(result, 'display')
    display.text = element.text
    sort = ET.SubElement(result, 'sort')
    sort.text = word
    return result


def output(elements):
    main_dir = {}
    for item in elements:
        if item.text:
            if item.tag in main_dir:
                main_dir[item.tag].append(item.text)
            else:
                main_dir[item.tag] = [item.text]
        else:
            sub_dir = {}
            for piece in item:
                sub_dir[piece.tag] = piece.text
            main_dir[item.tag] = sub_dir
    for key in main_dir:
        if len(main_dir[key]) == 1:
            main_dir[key] = main_dir[key][0]
    return main_dir


def find_content(container):
    tree = ET.parse(container)
    root = tree.getroot()
    for child in root.iter():
        if 'full-path' in child.attrib:
            content = child.attrib['full-path']
            return content


def process(arg, cwd=None):
    proc = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = proc.communicate()
    returncode = proc.returncode
    if returncode != 0:
        raise Exception(err)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print >> sys.stderr, 'Error occured', e
        sys.exit(1)

    sys.exit(0)
