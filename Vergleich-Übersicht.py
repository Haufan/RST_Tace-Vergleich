import os
import re


def main():

    _files_comp = os.listdir('Vergleiche')
    _files_rst = os.listdir('RST')
    _files_iter = range(len(_files_comp))

    for n in _files_iter:

        relation_difference_num = {}
        _liste_edus = ['']
        _num_order = []

        # liest Vergleichsdatei, überspring 1. Zeile
        f = open(os.path.join('Vergleiche', str(_files_comp[n])), "r", encoding="UTF-8")
        next(f)

        for line in f.readlines():
            # Selektiert nur Unterschiede
            if 'NRCA' not in line:
                # Extra Infos
                if 'No matching' in line:
                    _extra_info = '(no matching)'
                elif 'Partially identical CS' in line:
                    _extra_info = '(partial CS)'
                elif 'C1=C2 and A1=A2' in line:
                    _extra_info = '(switched CS)'
                elif '"N/S' in line:
                    _extra_info = '(switched dir)'
                else:
                    _extra_info = 0

                line = line.split(",")
                _temp_dict = {}
                # Relation
                _temp_relation = line[3] + ' vs ' + line[13]
                # EDU ID
                if line[6] == '':
                    _temp_number = line[16] + line[14] + line[19]
                else:
                    _temp_number = line[6] + line[4] + line[9]
                # nach Zahlen
                if _temp_number not in relation_difference_num:
                    _temp_dict[_temp_relation] = _extra_info
                    relation_difference_num[_temp_number] = _temp_dict
                else:
                    _temp_dict = relation_difference_num[_temp_number]
                    _temp_dict[_temp_relation] = _extra_info
                    relation_difference_num[_temp_number] = _temp_dict
            else:
                pass
        f.close()

        # EDUs einlesen
        g = open(os.path.join('RST', str(_files_rst[n])), "r", encoding="UTF-8")
        for x in g.readlines():
            if '<segment id=' in x:
                _edu = re.findall('>.*<', x)
                _edu = _edu[0][1:-1]
                _liste_edus.append(_edu)
        g.close()

        # Übersicht schreiben
        h = open(os.path.join('Export', str(_files_rst[n]) + '.csv'), "a", encoding='UTF-8')
        h.write('EDUs\t' + '\t' + 'Relationen\t' + '\n')

        for z in relation_difference_num.keys():
            h.write('\n' + z)
            for n in relation_difference_num[z]:
                _edus = re.split('[⟵|⟶|⟷]', z)
                h.write('\t\t' + n + '\t\t' + _liste_edus[int(_edus[0])] +
                        '\t' + _liste_edus[int(_edus[1])] + '\n')
                # falls Extrainfo
                if relation_difference_num[z][n] != 0:
                    h.write('\t\t' + relation_difference_num[z][n] + '\n')
                else:
                    pass
        h.close()


if __name__ == '__main__':
    main()
