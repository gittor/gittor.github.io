#encoding=utf8

# 执行这个文件，会在脚本所在路径，重新生成_sidebar.md

# 运行环境
#   python 3.x

# 输入：无
# 输出：直接覆盖_sidebar.md

import os
import sys

StarIndent = 4

def ShouldIgnore(file_or_path):
    '''
    Args:
        file_or_path: 文件名或路径名，相对于当前路径
    Returns:
        返回file_or_path是否应该被忽略
    '''
    ignored = ["jigsaw", ".git"]

    # print(file_or_path)

    for x in ignored:
        if os.path.samefile(file_or_path, x): return True

    return False

def getTitle():
    return "<!-- 由build_sidebar.py生成，勿手改 -->\n"

def getPathMD(parentpath, pathname, indent):
    '''
    Args:
        parentpath: 父路径。相对于根目录的路径
        pathname: 路径的名字
        indent: 这一行前空几个空格
    Returns:
        返回pathname对应的md内容
    '''
    address = pathname
    ret = ' '*indent + '* ' + address + '\n'
    return ret

def getFileMD(parentpath, fname, indent):
    '''
    Args:
        parentpath: 父路径。相对于根目录的路径
        fname: 文件名，带扩展名
        indent: 这一行前空几个空格
    Returns:
        返回fname对应的md内容
    '''
    link = os.path.join(parentpath, fname)
    address = '[%s](%s)'%(os.path.splitext(fname)[0], link)
    ret = ' '*indent + '* ' + address + '\n'
    return ret

def getPath(parentpath, pathname, indent):
    '''
    Args:
        parentpath: 父路径。相对于根目录的路径
        pathname: 本路径名称
        indent: 这一行前空几个空格
    Returns:
        返回整个pathname对应的md内容
    '''

    relative = os.path.join(parentpath, pathname)

    ret = getPathMD(parentpath, pathname, indent)

    for name in os.listdir(relative):
        sub = os.path.join(relative, name)
        if os.path.isdir(sub):
            if ShouldIgnore(sub): continue
            ret += getPath(relative, name, indent+StarIndent)

    for name in os.listdir(relative):
        if name.lower() == "home.md": continue

        sub = os.path.join(relative, name)
        if os.path.isfile(sub):
            if ShouldIgnore(sub): continue
            ret += getFileMD(relative, name, indent+StarIndent)

    return ret

def getTotalMD():
    '''
    返回新的_sidebar.md的所有内容
    '''
    ret = getTitle()

    for name in os.listdir("."):
        if os.path.isdir(name):
            if ShouldIgnore(name): continue
            ret += getPath(".", name, 0)

    return ret

def main():
    # 先把当前路径调整为脚本所在路径，以便于可以双击直接运行
    scriptdir = os.path.split(sys.argv[0])[0]
    os.chdir(scriptdir)
    
    with open("_sidebar.md", "w", encoding="utf8") as fout:
        data = getTotalMD()
        fout.write(data)

if __name__ == "__main__":
    main()
