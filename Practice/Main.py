# Author  : Bruce li
# Date    : 2019-11-03
# Describe: 模拟实现一个ATM + 购物商城程序
# Trouble : None


#     ·额度 15000或自定义
#     ·实现购物商城，买东西加入购物车，调用信用卡接口结账
#     ·可以提现，手续费5%
#     ·支持多账户登录
#     ·支持账户间转账
#     ·提供还款接口
#     ·ATM记录操作日志
#     ·记录每月日常消费流水
#     ·每月22号出账单，每月10号为还款日，过期未还，按欠款总额 万分之5 每日计息
#     ·提供管理接口，包括添加账户、用户额度，冻结账户等。。。
#     ·用户认证用装饰器

import Shopping, ATM
while True:
    print('='*60)
    print('1、ATM\n2、购物商城')
    print('=' * 60)
    choice = input('人生总会遇到很多个十字路口， 因而会有许多选择。虽然似乎毫无逻辑， 但这也需要你的选择==>:')
    if choice == '1':
        ATM.ATM_main()
        Shopping.main()
    elif choice == '2':
        Shopping.main()
    else:
        continue




