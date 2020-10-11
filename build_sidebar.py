#! /usr/bin/python
#encoding=utf8

# 执行这个文件，会在脚本所在路径，重新生成_sidebar.md

# 运行环境
#   python 3.x

# 参数：无
# 输出：直接覆盖_sidebar.md

import os
import sys

# ----------------------------------------------------------------
# 全局配置

# 导出markdown时，每行前面的空格有几个
StarIndent = 4

# 要导出的根目录文件夹
WantExport = [
    "游戏相关",
    "语言和思想",
    "工具研究",
]

# 不导出的文章和目录
Ignored = [
    "实践项目",
    r"工具研究\electron",
    r"工具研究\SimpleWeb",
]

# 草稿文章
Draft = [
    r"游戏相关\unity-shader.md",
]


# ----------------------------------------------------------------

def ShouldIgnore(file_or_path):
    '''
    Args:
        file_or_path: 文件名或路径名，相对于根目录
    Returns:
        返回file_or_path是否应该被忽略
    '''
    
    for x in Ignored:
        if os.path.samefile(file_or_path, x): return True

    return False

def IsDraft(file_or_path):
    for x in Draft:
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
    if IsDraft(link):
        address = '[%s(草稿)](%s)'%(os.path.splitext(fname)[0], link)
    else:
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

    for name in WantExport:
        ret += getPath(".", name, 0)

    return ret

def main():
    # 先把当前路径调整为脚本所在路径，以便于可以双击直接运行
    scriptdir = os.path.split(sys.argv[0])[0]
    if scriptdir:
        os.chdir(scriptdir)
    
    data = getTotalMD()

    with open("_sidebar.md", "w", encoding="utf8") as fout:
        fout.write(data)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input()
    
