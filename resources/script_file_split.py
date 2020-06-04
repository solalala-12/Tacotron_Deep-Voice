import os, getopt, sys

def main(argv):
    FILE_NAME = argv[0]
    TXT_FILE_NAME = ""

    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
                                 "hf:", ["help","file_name="])
    except getopt.GetoptError: # 옵션지정이 올바르지 않은 경우
        print(FILE_NAME, '-f <txt file name>')
        sys.exit(2)

    for opt, arg in opts: # 옵션이 파싱된 경우
        if opt in ("-h", "--help"): # HELP 요청인 경우 사용법 출력
            print(FILE_NAME, '-f <txt file name>')
            sys.exit()

        elif opt in ("-f", "--file_name"): # 인스턴명 입력인 경우
            TXT_FILE_NAME = arg

    if len(TXT_FILE_NAME) < 1: # 필수항목 값이 비어있다면
        print(FILE_NAME, "-f option is mandatory") # 필수임을 출력
        sys.exit(2)
    
    root_dir = '.'
    file_list = list()
    file_list.append(TXT_FILE_NAME)
    # file_list=['NB11097133', 'NB11100445', 'NB11101719', 'NB11102935', 'NB11104400', 'NB11107935', 'NB11109162', 'NB11110442', 'NB11111700', 'NB11114914', 'NB11116155', 'NB11117710', 'NB11118881', 'NB11121711', 'NB11122836', 'NB11124075', 'NB11125360', 'NB11128215', 'NB11129382', 'NB11131361', 'NB11133909', 'NB11135139', 'NB11136278', 'NB11137431', 'NB11141004', 'NB11142372', 'NB11143669', 'NB11146372', 'NB11147708', 'NB11149010', 'NB11150149', 'NB11153278', 'NB11154477', 'NB11155502', 'NB11156730', 'NB11159823', 'NB11161191', 'NB11162377', 'NB11163566', 'NB11166110', 'NB11167060', 'NB11167827', 'NB11173530', 'NB11174428', 'NB11175307', 'NB11176058', 'NB11179032', 'NB11179964', 'NB11180755', 'NB11183271', 'NB11183860', 'NB11184627', 'NB11185533', 'NB11187640', 'NB11188501', 'NB11189503', 'NB11190351', 'NB11192626', 'NB11194284', 'NB11195087', 'NB11197178', 'NB11198067', 'NB11199044', 'NB11199999', 'NB11202049', 'NB11202948', 'NB11203868', 'NB11204657', 'NB11207013', 'NB11207714', 'NB11208640', 'NB11209399', 'NB11211533', 'NB11212364', 'NB11214120', 'NB11216360', 'NB11217075', 'NB11218010', 'NB11218905', 'NB11221171', 'NB11221875', 'NB11222793', 'NB11223627', 'NB11225849', 'NB11226523', 'NB11227322', 'NB11229650', 'NB11230449', 'NB11231273', 'NB11231969', 'NB11234270', 'NB11234929', 'NB11235745', 'NB11236651', 'NB11238754', 'NB11239421', 'NB11240214', 'NB11241066', 'NB11243218', 'NB11243896', 'NB11244729', 'NB11245495', 'NB11247747', 'NB11248372', 'NB11249237', 'NB11252950', 'NB11253756', 'NB11254475', 'NB11256503', 'NB11257380', 'NB11258216', 'NB11259128']
    # file_list=file_list[0]
    ext = '.txt'

    for file in file_list:
        txt_file = os.path.join(root_dir, file+ext)
        under_index = 1
        normal_index = 1
        with open(txt_file, 'rt', encoding='UTF8') as f:
            for i, text in enumerate(f):
                result_file = None
                if text.find('_') > -1: # 첫 문자에 언더바가 있으면!
                    result_file = open(os.path.join(root_dir, '_'+file+' (' + str(under_index) + ')' + ext), 'w')
                    under_index = under_index + 1
                else: # 없으면!
                    result_file = open(os.path.join(root_dir, file+' (' + str(normal_index) + ')' + ext), 'w')
                    normal_index = normal_index + 1
                result_file.write(text.replace('_','').strip('\n'))
            result_file.close()

if __name__ == "__main__":
    main(sys.argv)