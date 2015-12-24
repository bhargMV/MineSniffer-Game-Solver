import sys
import itertools
import copy

#stores minesniffer board configuration
board = []

#stores variable names for each mine
vars = []
N = 0
M = 0
Num_Vars = 0


def parse_file(filename):
    # read the layout file to the board array

    f = open(filename)
    line1 = f.readline()

    line1_c = [x.strip() for x in line1.replace(';','').split(' ')]


    global N
    N = int(line1_c[0])

    global M
    M = int(line1_c[1])

    global board
    board = []

    for i in range(0, N):
        line = f.readline()
        line_c = []

        for x in line.split(','):
            if x == '':
                break

            if x.strip() == 'X':
                line_c.append(-1)

            else:
                line_c.append(int(x))

        board.append(line_c)

    board.reverse()

    var_num = 1

    for i in range(0, N):
          temp = []

          for j in range(0, M):
            if(board[i][j] == -1):
                temp.append(var_num)
                var_num = var_num + 1
            else:
                temp.append(-1)

          vars.append(temp)

    global Num_Vars
    Num_Vars = var_num - 1
    #print "VARS", vars

    f.close()
    return board


#gets the list of mines around i, j cell
def getMinesAroundMe(i, j):
    v = []
    global vars

    for k in range(i-1, i+2):
        for l in range(j-1, j+2):
            if k < 0 or k >=N or l <0 or l >= M:
                continue
            else:
                if vars[k][l] != -1:
                    v.append(vars[k][l])

    return v


def convert2CNF(board, output):
    # interpret the number constraints
    fout = open(output, 'w')

    cnf = []

    for i in range(0, N):
          for j in range(0, M):

              if board[i][j] == -1:
                  continue

              var_sur = getMinesAroundMe(i,j)
              #print var_sur

              if board[i][j] > len(var_sur):
                    print "Board in Inconsistent"
                    return


              for p in range(0, len(var_sur)+1):
                  if p == board[i][j]:
                      continue

                  ncr = list(itertools.combinations(var_sur, p))

                  for k in range(0, len(ncr)):
                      temp = copy.deepcopy(var_sur)
                      temp1 = list(ncr[k])

                      for m in range(0, len(temp)):
                          if temp[m] in temp1:
                              temp[m] = -1 * temp[m]

                      if temp not in cnf:
                        cnf.append(temp)


    f_cnf = cnf
    #print f_cnf

    #Code to write to file
    fout.write("p cnf " + str(Num_Vars) + " " + str(len(f_cnf)) + " \n");
    for i in range(0, len(f_cnf)):
        for j in range(0, len(f_cnf[i])):
                fout.write(str(f_cnf[i][j]) + " ");

        fout.write("0 \n");

    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])

        #print board
    convert2CNF(board, sys.argv[2])