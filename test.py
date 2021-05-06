import inquirer
# encoding: utf-8

def correct_backspace(S):
    q = []

    for i in range(0, len(S)):

        if S[i] != '\x08':
            q.append(S[i])
        elif len(q) != 0:
            q.pop()

            # Build final string
    ans = ""

    while len(q) != 0:
        ans += q[0]
        q.pop(0)

        # return final string
    return ans

queation = [inquirer.Text('kek', message='Hey').encode('utf-8').strip()]
anwser = inquirer.prompt(queation)
print(correct_backspace(anwser['kek']))