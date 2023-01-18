def removeBlank(filename: str):
    try:
        with open(filename) as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
        lines = [line for line in lines if line != '']
        return '\n'.join(lines)
    except:
        return ''

if __name__ == '__main__':
    with open('.\data\lbuild_st.txt', 'w') as f:
        print(removeBlank('.\data\lbuild_20230117.txt'), file=f)
