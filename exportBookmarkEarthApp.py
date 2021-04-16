#coding:utf-8
import sqlite3

# 获取书签内容
def genBookmark(href, addDate, icon, title):
    return '''
<DL><p>
<DT><A HREF="%s" ADD_DATE="%s" ICON="%s">%s</A>'''%(href, addDate, icon, title)

# 获取文件夹内容
def getFolder(addDate, lastModify, title):
    return '''
<DL><p>
<DT><H3 ADD_DATE="%s" LAST_MODIFIED="%s">%s</H3>'''%(addDate, lastModify, title)

# 生成书签结构
def genContent(parentId, c):
    content = ''
    sql = '''
    SELECT
        id,
        title,
        icon,
        url,
        parent_id,
        add_date,
        last_modified
    FROM
        bookmark 
    WHERE parent_id = %s
    '''%(parentId)
    # 生成目录
    c.execute(sql + "AND type = 2")
    folders = c.fetchall()
    for row in folders:
        content += getFolder(row[5], row[6], row[1]) + genContent(row[0], c) + "\n</DL><p>"
    # 生成书签
    marks = c.execute(sql + "AND type = 1")
    for mark in marks:
        content += genBookmark(mark[3], mark[5], mark[2], mark[1])
    return content

# 建立数据库连接
conn = sqlite3.connect("bookmark_earth_db.db")
c = conn.cursor()
# 导出文件名
htmlFileName = "bookmarks.html"
f = open(htmlFileName, 'w', encoding="utf-8")
# 文件内容框架
htmlContent = '''
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
<DT><H3 ADD_DATE="1598108393" LAST_MODIFIED="1605607896" PERSONAL_TOOLBAR_FOLDER="true">书签栏</H3>
%s
</DL><p>
'''%(genContent(-1, c))
# 写出与释放
f.write(htmlContent)
f.close
conn.close()