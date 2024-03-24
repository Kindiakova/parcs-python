from Pyro4 import expose

class Solver:
    
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        
        module = 2 ** 31 - 1
        p = 31
        
        s = self.read_input()
        leng = len(s)
        n = len(self.workers)
        sub_leng = leng // n
        
        # map
        mapped = []
        for i in range(0, n):
            substring = s[(i*sub_leng):(i*sub_leng + sub_leng)]
            mapped.append(self.workers[i].mymap(i, substring, p, module))

        print ('Map finished: ', mapped)

        # reduce
        step = pow(p, sub_leng, module)
        reduced = self.myreduce(mapped, step, module)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(i, s, p, module):
        print(i, s)
        hash_value = 0
        p_pow = 1
        for c in s:
            hash_value = (hash_value + ((ord(c) - ord('a') + 1) * p_pow % module) ) % module
            p_pow = (p_pow * p) % module
            
        return hash_value
        

    @staticmethod
    @expose
    def myreduce(mapped, step, module):
        delt = 1
        output = 0
        for x in mapped:
            output = (output + (x.value * delt % module) ) % module
            delt = delt * step % module
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return line

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
