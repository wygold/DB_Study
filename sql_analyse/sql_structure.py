class SqlStructure:
    '''breaking_keywords = ['(','union']'''

    LEFT_BRACKET = '('
    RIGHT_BRACKET = ')'

    original_sql_string = ''

    remaining_sql_strings = []

    inner_sql_strings = []

    inner_sql_structures = []

    def __init__(self, sql_string):
        self.original_sql_string = sql_string

    def initialize_structure(self):
        '''find first left bracket'''
        current_remain_sql =''
        current_inner_sql =''
        left_bracket_counter = 0

        for char in self.original_sql_string:
            if char <> self.LEFT_BRACKET and char <> self.RIGHT_BRACKET and left_bracket_counter ==0:
                current_remain_sql = current_remain_sql + char
            elif char <> self.LEFT_BRACKET and char <> self.RIGHT_BRACKET and left_bracket_counter > 0:
                current_inner_sql = current_inner_sql + char

            if char == self.LEFT_BRACKET and left_bracket_counter ==0:
                self.remaining_sql_strings.append(current_remain_sql)
                current_remain_sql = ''
                left_bracket_counter = left_bracket_counter + 1
            elif char == self.LEFT_BRACKET and left_bracket_counter > 0:
                current_inner_sql = current_inner_sql + char
                left_bracket_counter = left_bracket_counter + 1

            if char  == self.RIGHT_BRACKET and left_bracket_counter > 1:
                current_inner_sql = current_inner_sql + char
                left_bracket_counter = left_bracket_counter - 1
            elif char  == self.RIGHT_BRACKET and left_bracket_counter == 1:
                self.inner_sql_strings.append(current_inner_sql)
                current_inner_sql=''
                left_bracket_counter = left_bracket_counter - 1

        if current_remain_sql <> '':
            self.remaining_sql_strings.append(current_remain_sql)
            current_remain_sql = ''

        print self.remaining_sql_strings
        print self.inner_sql_strings

d=SqlStructure('select (sd(adfaf)f)asf(as(adf(asdf))f) (asfd)maaa')
d.initialize_structure()