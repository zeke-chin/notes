```yaml
version: '2'
services:
  mysql:
    restart: always
    image: mysql
    container_name: mysql
    volumes:
      - /apps/mysql/mydir:/mydir
      - /apps/mysql/datadir:/var/lib/mysql
      - /apps/mysql/conf/my.cnf:/etc/my.cnf
      # 数据库还原目录 可将需要还原的sql文件放在这里
      - /apps/mysql/source:/docker-entrypoint-initdb.d
    environment:
      - "MYSQL_ROOT_PASSWORD=113113"
      - "MYSQL_DATABASE=frs"
      - "TZ=Asia/Shanghai"
    ports:
      # 使用宿主机的3306端口映射到容器的3306端口
      # 宿主机：容器
      - 3306:3306
```