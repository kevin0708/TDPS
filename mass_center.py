class MassCenter():
    def __init__(self, line_number, line_thick, abandon_line_number):
        #assert line_number >= abandon_line_number, 'line number must greater or equal to abandoned line number'

        line_gap = math.floor(320 / line_number)
        first_line_pos = round(line_gap / 2)-1
        left_line_thick = math.ceil((line_thick - 1) / 2)
        right_line_thick = math.floor((line_thick - 1) / 2)
        self.extract_line_list = []
        for i in range(line_number):
            middle_pos = first_line_pos + i * line_gap
            self.extract_line_list.extend([i for i in range(middle_pos-left_line_thick, middle_pos+right_line_thick+1)])
        print(self.extract_line_list)
        self.abandon_line_number = abandon_line_number

    def run(self, flatten_image):
        his = []
        for i in range(len(self.extract_line_list)):
            cur_index = self.extract_line_list[i]
            his.append(0)
            his[i] += flatten_image[cur_index]
            for j in range(239):
                cur_index += 320
                his[i] += flatten_image[cur_index]


        if self.abandon_line_number != 0:
            sort_list, sort_index = bubble_sort(his)
            for i in range(self.abandon_line_number):
                his[sort_index[i]] = 0

        print(his)

        half_his = round(sum(his)/2)
        print(half_his)
        number = 0

        for i in range(len(his)):
            number += his[i]
            if number >= half_his:
                return self.extract_line_list[i]

def bubble_sort(input_list):
    alist = input_list.copy()
    length = len(alist)
    line_list = list(range(length))

    for i in range(length - 1):
        # i表示比较多少轮
        for j in range(length - i - 1):
            # j表示每轮比较的元素的范围，因为每比较一轮就会排序好一个元素的位置，
            # 所以在下一轮比较的时候就少比较了一个元素，所以要减去i
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
                line_list[j], line_list[j + 1] = line_list[j + 1], line_list[j]
    return alist, line_list

mass_center_class = MassCenter(20, 5, 80)