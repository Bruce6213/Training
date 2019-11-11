# Author  : Bruce li
# Date    : 2019-11-04
# Describe: ATM机模拟
# Trouble : None


import logging, random
format='%(asctime)s %(message)s'
logging.basicConfig(filename='ATM_LOGGING', level='DEBUG', format = '%(asctime)s %(message)s')
# 账号与密码
cart = {9999:10000000000, 2019:2019, 2018:2018, 2017:2017, 2020:2020}
# 额度
limit = {2017:5000, 2018:8000, 2019:15000, 2020:20000, 9999:10000}
# 已登入的账号
exist = []
# ATM界面显示
def Show():
    list = ["额度查询", "账号登入", "冻结账户", "转账", "取款", "还款", "离开"]
    for i in list:
        print(list.index(i) + 1, '、', i)
    choice = int(input('==>'))
    return choice
# 用户认证(装饰器)
def wran(func):
    def inner():
        res2 = func()
        while True:
            temp = random.randint(1000, 9999)
            res = int(input('请输入验证码%d: '%temp))
            if res == temp:
                print('账号登入成功'.center(60, '*'))
                return res2
            else:
                print('验证码错误!'.center(60, '*'))
                continue
    return inner
# 账户登入
@wran
def enter():
    while True:
        account = int(input('请输入你的账号:'))
        password = int(input('请输入你的密码:'))
        if account in exist:
            print('请不要重复登入同一个账号'.center(60, '*'))
        else:
            if cart.get(account):
                if limit.get(account):
                    if cart[account] == password:
                        logging.debug("账号: %d登入成功"%account)
                        exist.append(account)
                        break
                else:
                    print('账号%d已被冻结'.center(60, '*')%account)
                    return False
            print('账号或密码错误'.center(60, '*'))
    return account
# 选择要执行操作的账号
# 当flag为1时表示不需要进行账号的登入
def choise_account(flag = 0):
    global temp_index
    if exist:
        print('=' * 60)
        for i in exist:
            print(exist.index(i) + 1, '、使用第', exist.index(i) + 1, '个账号: ', i)
            temp_index = exist.index(i) + 1
        print(temp_index + 1, '、使用其它账号')
        print('=' * 60)
        choice = int(input('==>'))
    else:
        if flag == 0:
            return enter()
        return int(input('请输入您准备还款的账号:'))
    if choice == temp_index + 1:
        if flag == 0:
            return enter()
        return int(input('请输入您准备还款的账号:'))
    else:
        account_name = exist[choice - 1]
        return account_name
# 金额流出操作
def account_out(send, recv = 1111, money = 0):
    if recv == 1111:
        receive = int(input('请输入您转入的账号:'))
    else:
        receive = recv
    if cart.get(receive):
        if money == 0:
            num = float(input('请输入您转出的金额:'))
        else:
            num = money
        # 给予每张信用卡透支5000的额度
        if limit[send] - num >= -5000:
            limit[receive] += num
            limit[send] -= num
            print('转账成功'.center(60, '*'))
            logging.debug("账号: %d向账号: %d转账%.2f元"%(send, receive, num))
        else:
            print('世界这么大, 口袋这么小，钱就这么少, 想法却真多呀'.center(60, '*'))
    else:
        print('该账户不存在')
# 支付接口
def pay(money):
    using_account = choise_account()
    if using_account:
        account_out(using_account, 9999, money)
        return using_account
    else:
        return False
# 还款接口
def ATM_repayment():
    using_account = choise_account(1)
    if cart.get(using_account):
        sum = float(input('请输入您准备还款的金额:'))
        limit[using_account] += sum
        logging.debug('账号: %d还款%.2f元' % (using_account, sum))
        print('还款成功'.center(60, '*'))
    else:
        print('该账户不存在')
# 欠款未还， 计算利息
def interest():
    for i in exist:
        if limit[i] < 0:
            limit[i] *= 1.00005
# 主函数——接口
def ATM_main():
    while True:
        num = Show()
        # 额度查询
        if num == 1:
            while True:
                if exist:
                    print('*'*60)
                    for i in exist:
                        print('账号:%-5d\t额度:%-6d'%(i, limit[i]))
                    print('*' * 60)
                    break
                else:
                    if not enter():
                        break
        # 账号登入
        elif num == 2:
            if not enter():
                continue
        # 账号冻结
        elif num == 3:
            temp = int(input('请输入您准备冻结的账号: '))
            temp2 = int(input('请输入您准备冻结的账号的密码: '))
            if cart.get(temp):
                if cart[temp] == temp2:
                    del limit[temp]
                    if temp in exist:
                        exist.remove(temp)
                    print('冻结账号成功'.center(60, '*'))
                else:
                    print('密码输入错误, 冻结账号失败'.center(60, '*'))
            else:
                print('未检测到该账户的存在'.center(60, '*'))
        # 转账
        elif num == 4:
            send = choise_account()
            if not send:
                continue
            else:
                account_out(send)
        # 取款
        elif num == 5:
            using_account = choise_account()
            if not using_account:
                continue
            else:
                sum = float(input('请输入您需要取款的金额（手续费5%）:'))
                limit[using_account] -= sum * 1.05
                print('取款成功'.center(60, '*'))
                logging.debug('账号: %d取款%.2f元'%(using_account, sum))
        # 还款
        elif num == 6:
            using_account = choise_account(1)
            if limit.get(using_account):
                if cart.get(using_account):
                    sum = float(input('请输入您准备还款的金额:'))
                    limit[using_account] += sum
                    logging.debug('账号: %d还款%.2f元'%(using_account, sum))
                    print('还款成功'.center(60, '*'))
                else:
                    print('该账户不存在')
            else:
                print('账号%d已被冻结'.center(60, '*') % using_account)
                continue
        # 离开ATM机
        elif num == 7:
            print('欢迎下来光临！')
            break
        # 无效输入
        else:
            print('what are you doing!')
            continue
if __name__ == '__main__':
    ATM_main()