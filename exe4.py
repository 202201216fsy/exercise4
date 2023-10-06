import sqlite3

# 连接到数据库
conn = sqlite3.connect('library.db')
c = conn.cursor()

# 创建表
c.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

# 交互式菜单
while True:
    print('请选择一个操作:')
    print('1. 添加书籍')
    print('2. 查找书籍详细信息')
    print('3. 查找预订状态')
    print('4. 查找所有书籍')
    print('5. 更新书籍详细信息')
    print('6. 删除书籍')
    print('7. 退出')

    choice = input('选择操作 (1-7): ')

    if choice == '1':
        # 添加图书
        book_id = input('请输入图书编号: ')
        title = input('请输入标题: ')
        author = input('请输入作者: ')
        isbn = input('请输入ISBN: ')
        status = input('请输入状态: ')

        c.execute('INSERT INTO Books VALUES (?, ?, ?, ?, ?)', (book_id, title, author, isbn, status))
        conn.commit()
        print('图书已成功添加到数据库！')

    elif choice == '2':
        # 查找图书详细信息
        book_id = input('请输入图书编号: ')

        c.execute('''
            SELECT Books.*, Reservations.ReservationID, Users.UserID
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (book_id,))
        book_info = c.fetchone()

        if book_info:
            print('图书详细信息:')
            print('编号:', book_info[0])
            print('标题:', book_info[1])
            print('作者:', book_info[2])
            print('ISBN:', book_info[3])
            print('状态:', book_info[4])
            print('预订状态:', '已预订' if book_info[5] else '未预订')
            print('用户预订状态:', book_info[6] if book_info[6] else '未预订')
        else:
            print('找不到该图书。')

    elif choice == '3':
        # 查找预订状态
        search_id = input('请输入BookID、Title或UserID: ')

        if search_id.startswith('LB'):
            # 根据BookID查找预订状态
            c.execute('SELECT ReservationID FROM Reservations WHERE BookID = ?', (search_id,))
            reservation_id = c.fetchone()

            if reservation_id:
                print('图书已被预订，预订ID:', reservation_id[0])
            else:
                print('图书未被预订。')
        elif search_id.startswith('LU'):
            # 根据UserID查找预订状态
            c.execute('SELECT ReservationID FROM Reservations WHERE UserID = ?', (search_id,))
            reservation_id = c.fetchone()

            if reservation_id:
                print('用户已预订图书，预订ID:', reservation_id[0])
            else:
                print('用户未预订图书。')
        elif search_id.startswith('LR'):
            # 根据ReservationID查找预订状态
            c.execute('SELECT BookID FROM Reservations WHERE ReservationID = ?', (search_id,))
            book_id = c.fetchone()

            if book_id:
                print('预订ID:', search_id, '对应的图书编号:', book_id[0])
            else:
                print('找不到该预订ID。')
        else:
            print('输入无效。')

    elif choice == '4':
        # 查找所有书籍
        c.execute('SELECT * FROM Books')
        books = c.fetchall()

        print('所有图书:')
        for book in books:
            print('编号:', book[0])
            print('标题:', book[1])
            print('作者:', book[2])
            print('ISBN:', book[3])
            print('状态:', book[4])
            print('------')

    elif choice == '5':
        # 更新图书详细信息
        book_id = input('请输入图书编号: ')

        c.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
        book = c.fetchone()

        if book:
            print('当前图书详细信息:')
            print('编号:', book[0])
            print('标题:', book[1])
            print('作者:', book[2])
            print('ISBN:', book[3])
            print('状态:', book[4])

            new_title = input('请输入新标题 (按回车键跳过): ')
            new_author = input('请输入新作者 (按回车键跳过): ')
            new_isbn = input('请输入新ISBN (按回车键跳过): ')
            new_status = input('请输入新状态 (按回车键跳过): ')

            if new_title or new_author or new_isbn or new_status:
                # 更新图书信息
                c.execute('''
                    UPDATE Books
                    SET Title = COALESCE(?, Title),
                        Author = COALESCE(?, Author),
                        ISBN = COALESCE(?, ISBN),
                        Status = COALESCE(?, Status)
                    WHERE BookID = ?
                ''', (new_title, new_author, new_isbn, new_status, book_id))
                conn.commit()
                print('图书信息已更新。')
            else:
                print('没有提供新的信息，图书信息未更改。')
        else:
            print('找不到该图书。')

    elif choice == '6':
        # 删除图书
        book_id = input('请输入要删除的图书编号: ')

        c.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
        book = c.fetchone()

        if book:
            c.execute('DELETE FROM Books WHERE BookID = ?', (book_id,))
            c.execute('DELETE FROM Reservations WHERE BookID = ?', (book_id,))
            conn.commit()
            print('图书已成功删除。')
        else:
            print('找不到该图书。')

    elif choice == '7':
        # 退出程序
        conn.close()
        break

    print('----------------------------')

print('程序已退出。')