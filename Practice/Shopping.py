# Author  : Bruce li
# Date    : 2019-11-03
# Describe: 购物商城
# Trouble : None


import time
from ATM import *
produce = {
        '深入理解计算机系统':{
            '价格': 119.9,
            '库存': 100,
            '销量': 1500,
            '店铺名称': '京东自营'
        },
        'python编程': {
            '价格': 59.9,
            '库存': 1000,
            '销量': 150,
            '店铺名称': 'python自营店'
        },
        '线性代数': {
            '价格': 99.9,
            '库存': 1050,
            '销量': 50,
            '店铺名称': '线代旗舰店'
        },
        '1': {
            '价格': 29.9,
            '库存': 10050,
            '销量': 5000,
            '店铺名称': '新华旗舰店'
        }
    }
# 商品列表
def Goods(produce, ShoppingCar):
    while True:
        index = 1
        print('\n' + '热销商品, 双十一抢购'.center(60, '*'))
        for i in produce.keys():
            print(str(index) + '、', i)
            index = index + 1
        print(str(index) + '、 Exit')
        choice = input('==>(商品名称)')
        if choice.lower() == 'exit':
            break
        elif produce.get(choice):
            print('商品信息'.center(60, '*'))
            for i, j in produce[choice].items():
                print(i, ':', j)
            print('='*60)
            print('1、加入购物车  OR  2、关闭该页面'.center(60))
            reply = input('==>')
            if reply == '1':
                num = int(input('您需要加几件该商品与您的购物车中?'))
                for i in ShoppingCar:
                    if i.get(choice):
                        i[choice] += num
                        break
                else:
                    dict = {choice : num}
                    ShoppingCar.append(dict)
                print('亲, 记得最后付款哦！')
            elif reply == '2':
                continue
            # 如何处理输入除1与2以外的数字
            else:
                pass
        else:
            print('页面走丢了。。。')
# 查看购物车
def LookCar(ShoppingCar):
    print('您的购物车'.center(60, '*'))
    if ShoppingCar:
        for i in ShoppingCar:
            # 此处有什么办法可以改进?
            for j, k in i.items():
                print("'名称': %-10s, '数量': %4d" %(j, k))
    else:
        print('亲，这是双十一哟，一年只有一次哟，不买点东西可惜哟！')
# 计算总金额
def Sum(ShoppingCar, produce):
    sum = 0.0
    for i in ShoppingCar:
        for j in i.keys():
            sum += i[j] * produce[j]['价格']
    return sum
def store(ShoppingCar):
    print('淘乐堡, 往哪跑!'.center(60, '-'))
    while True:
        Goods(produce, ShoppingCar)
        if not ShoppingCar:
            print('弹出窗口'.center(60, '*'))
            print('1、 那就不让自己有遗憾！')
            print('2、 唉， 生活不易，我编Python。。。')
            reply = int(input('==>'))
            if reply == 1:
                continue
            else:
                print('客观······再看看马')
                break
        else:
            LookCar(ShoppingCar)
            print('总计:%.2f'%Sum(ShoppingCar, produce))
            print('亲, 天时地利人和哦！')
            print('1、 付款')
            print('2、 刚想起来，我还有点东西没买到')
            print('3、 我先查看一下我名下还有多少资产')
            print('4、 东西不买了')
            choice = int(input('==>'))
            if choice == 1:
                using_account = pay(Sum(ShoppingCar, produce))
                if using_account:
                    with open('日常消费记录', 'a') as file:
                        file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '     账号: %d在淘乐堡商城消费了%.2f元\n'%(using_account, Sum(ShoppingCar, produce)))
                    print('客观，慢走，欢迎下次再来。')
                    break
                else:
                    print('账号被冻结， 付款失败'.center(60, '*'))
                    continue
            elif choice == 3:
                ATM_main()
            elif choice == 4:
                print('你无情,你残酷,你无理取闹!')
                break
            else:
                continue
# 显示账单
def ShowBill():
    with open('日常消费记录', 'r') as file:
        res = file.readlines()
        return res
# 判断是否需要还款
def repayment():
    if exist:
        for i in exist:
            if limit[i] < 0:
                print('您的账号%d已经欠款%.2f元, 若今日未还，将按欠款总额万分之5每日计息'.center(60, '*')%(i, -limit[i]))
        return True
    else:
        return False
# 主函数——接口
def main():
    day = 1
    month = 1
    # 使用标志变量flag表示上个月是否消费过
    flag = 0
    # 使用标志变量flag2表示是否有欠款未还
    flag2 = False
    # 存储上个月的账单
    res = ''
    while True:
        # 假设一个月只有5天
        if day > 5:
            month += 1
            flag = 1
            if month > 12:
                month = 1
            day = 1
            res = ShowBill()
            with open('日常消费记录', 'w') as file:
                pass
            print('\n' + '新的月份已来临'.center(60, '='))
        else:
            print('\n' + '新的一天已来临'.center(60, '='))
            # 2号出账单
            if day == 2:
                print('上个月的消费账单'.center(60, '*'))
                if flag == 1:
                    for i in res:
                        print(i)
            # 4号为还款日，过期未还，按欠款总额 万分之5 每日计息
            elif day == 4:
                if flag == 1:
                    if repayment():
                        print('是否立刻还款?(Y/N)')
                        reply = input('==>')
                        if reply.lower() == 'y':
                            ATM_repayment()
                        else:
                            print('出来混的， 始终是要还的！！！'.center(60, '*'))
                            flag2 = True
        # 购物车
        ShoppingCar = []
        store(ShoppingCar)
        if flag2:
            interest()
        print('一天结束, 早点睡觉！！！'.center(60, '='))
        day += 1
        time.sleep(2)
if __name__ == '__main__':
    main()






