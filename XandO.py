def print_fig(fig):
    for i in range(len(fig)):
        if fig[i] == '':
            print('_',end='')
        else:
            print(fig[i],end='')
        if i == 2 or i == 5 or i == 8:
            print('')
        else:
            print('|',end='')
def check_fig(fig):
    winest = [[0,1,2], [3,4,5], [6,7,8], [0,4,8], [2,4,6], [0,3,6], [1,4,7], [2,5,8]]
    for i in winest:
        if fig[i[0]] == fig[i[1]] and fig[i[1]] == fig[i[2]] and '_' not in fig[i[0]] and fig[i[0]] != '':
            if fig[i[0]] == 'X':
                print('Player №1 WIN!')
            else:
                print('Player №2 WIN!')
            return True
#print(fig)
fig = list('' for x in range(0, 9))
win = False
while not win:
    i=1
    while i < 3:
        try:
            answer = int(input(f'Player №{i} your move? '))
        except:
            print('Please enter Integer 0..8!')
            continue
        if answer not in range(0, 9):
            print('Please enter Integer 0..8!')
            continue
        if fig[answer] != '':
            print(f'In this cell already have move={fig[answer]}')
            continue
        if i==1:
            fig[answer] = 'X'
        else:
            fig[answer] = 'O'
        print_fig(fig)
        win = check_fig(fig)
        if win:
            break
        i+=1



