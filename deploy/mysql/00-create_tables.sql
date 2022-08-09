use fa_demo;

create table if not exists access
(
    id                    int auto_increment
        primary key,
    create_time           datetime(6) default CURRENT_TIMESTAMP(6) not null comment '创建时间',
    update_time           datetime(6) default CURRENT_TIMESTAMP(6) not null on update CURRENT_TIMESTAMP(6) comment '更新时间',
    path                  varchar(255)                             null comment '路径',
    component             varchar(255)                             null comment '组件',
    name                  varchar(255)                             not null comment '名称',
    title                 varchar(255)                             not null comment '标题',
    icon                  varchar(255)                             null comment '图标',
    is_button             tinyint(1)  default 0                    not null comment '是否为按钮',
    scopes                varchar(255)                             null comment '权限范围标识',
    parent_id             int         default 0                    not null comment '父id',
    order_no              int         default 999                  null comment '用来排序的序号',
    is_router             tinyint(1)  default 1                    not null comment '是否为前端路由',
    hide_menu             tinyint(1)  default 0                    not null comment '当前路由不再菜单显示',
    status                tinyint(1)  default 1                    not null comment 'True:启用 False:禁用',
    remark                varchar(255)                             null comment '备注描述',
    redirect              varchar(255)                             null comment '重定向',
    hide_children_in_menu tinyint(1)  default 0                    not null comment '隐藏所有子菜单',
    constraint name
        unique (name),
    constraint scopes
        unique (scopes),
    constraint title
        unique (title)
)
    comment '权限表';

create table if not exists aerich
(
    id      int auto_increment
        primary key,
    version varchar(255) not null,
    app     varchar(100) not null,
    content json         not null
);

create table if not exists role
(
    id          int auto_increment
        primary key,
    create_time datetime(6) default CURRENT_TIMESTAMP(6) not null comment '创建时间',
    update_time datetime(6) default CURRENT_TIMESTAMP(6) not null on update CURRENT_TIMESTAMP(6) comment '更新时间',
    role_name   varchar(15)                              not null comment '角色名称',
    order_no    int         default 999                  null comment '用来排序的序号',
    status      tinyint(1)  default 1                    not null comment 'True:启用 False:禁用',
    remark      varchar(255)                             null comment '备注描述'
)
    comment '角色表';

create table if not exists role_access
(
    role_id   int not null,
    access_id int not null,
    constraint role_access_ibfk_1
        foreign key (role_id) references role (id)
            on delete cascade,
    constraint role_access_ibfk_2
        foreign key (access_id) references access (id)
            on delete cascade
);

create index access_id
    on role_access (access_id);

create index role_id
    on role_access (role_id);

create table if not exists user
(
    id           int auto_increment
        primary key,
    create_time  datetime(6) default CURRENT_TIMESTAMP(6) not null comment '创建时间',
    update_time  datetime(6) default CURRENT_TIMESTAMP(6) not null on update CURRENT_TIMESTAMP(6) comment '更新时间',
    username     varchar(20)                              not null comment '用户名',
    password     varchar(255)                             not null comment '密码',
    nickname     varchar(255)                             null comment '昵称',
    phone        varchar(11)                              null comment '手机号',
    email        varchar(255)                             null comment '邮箱',
    full_name    varchar(255)                             null comment '姓名',
    is_superuser tinyint(1)  default 0                    not null comment '是否为超级管理员',
    head_img     varchar(255)                             null comment '头像',
    gender       smallint    default 0                    not null comment 'unknown: 0
male: 1
female: 2',
    order_no     int         default 999                  null comment '用来排序的序号',
    status       tinyint(1)  default 1                    not null comment 'True:启用 False:禁用',
    remark       varchar(255)                             null comment '备注描述',
    constraint email
        unique (email),
    constraint phone
        unique (phone),
    constraint username
        unique (username)
)
    comment '用户表';

create table if not exists profile
(
    id          int auto_increment
        primary key,
    create_time datetime(6) default CURRENT_TIMESTAMP(6) not null comment '创建时间',
    update_time datetime(6) default CURRENT_TIMESTAMP(6) not null on update CURRENT_TIMESTAMP(6) comment '更新时间',
    point       int         default 0                    not null comment '积分',
    user_id     int                                      not null,
    order_no    int         default 999                  null comment '用来排序的序号',
    status      tinyint(1)  default 1                    not null comment 'True:启用 False:禁用',
    remark      varchar(255)                             null comment '备注描述',
    constraint user_id
        unique (user_id),
    constraint fk_profile_user_80190c5a
        foreign key (user_id) references user (id)
            on delete cascade
)
    comment '用户扩展资料';

create table if not exists user_role
(
    user_id int not null,
    role_id int not null,
    constraint user_role_ibfk_1
        foreign key (user_id) references user (id)
            on delete cascade,
    constraint user_role_ibfk_2
        foreign key (role_id) references role (id)
            on delete cascade
);

create index role_id
    on user_role (role_id);

create index user_id
    on user_role (user_id);

