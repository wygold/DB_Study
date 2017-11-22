import re

class SqlBlock:
    # static variables
    LEFT_BRACKET = '('
    RIGHT_BRACKET = ')'
    SQL_SET_OPERATORS = 'union|unionall|minus|intersect'

    original_sql_string = ''
    pre_processed_sql_string = ''

    outer_sql_strings = []
    inner_sql_strings = []
    inner_sql_blocks = []

    def __init__(self, sql_string):
        self.original_sql_string = sql_string
        self.outer_sql_strings = []
        self.inner_sql_strings = []
        self.inner_sql_blocks = []
        self.initialize_sql_block()

    def initialize_sql_block(self):
        self.pre_process_sql_block()

        self.breakdown_sql_by_brackets()
        self.breakdown_sql_by_set_operators()

        for innersql in self.inner_sql_strings:
            inner_sql_block = SqlBlock(innersql)
            inner_sql_block = inner_sql_block.initialize_sql_block()
            self.inner_sql_blocks.append(inner_sql_block)

        return self

    def pre_process_sql_block(self):
        # remove extra whitespace between words
        self.pre_processed_sql_string=" ".join(self.original_sql_string.split())

        # remove initial brackets if from upper level sql block
        if self.pre_processed_sql_string[0] == self.LEFT_BRACKET and \
            self.pre_processed_sql_string[-1] == self.RIGHT_BRACKET:
            self.pre_processed_sql_string = self.pre_processed_sql_string[1:-1]

        # change the original sql string to lower case
        self.pre_processed_sql_string=str.lower(self.pre_processed_sql_string)

        # change union all to unionall for original sql string
        # for word in original_sql_string
        self.pre_processed_sql_string.replace('union all', 'unionall')

    def breakdown_sql_by_brackets(self):
        # to break down the original SQL by brackets
        # this is to run first
        current_outer_sql = ''
        current_inner_sql = ''
        left_bracket_counter = 0

        for char in self.pre_processed_sql_string:
            if char <> self.LEFT_BRACKET and char <> self.RIGHT_BRACKET and left_bracket_counter ==0:
                current_outer_sql = current_outer_sql + char
            elif char <> self.LEFT_BRACKET and char <> self.RIGHT_BRACKET and left_bracket_counter > 0:
                current_inner_sql = current_inner_sql + char

            if char == self.LEFT_BRACKET and left_bracket_counter ==0:
                self.outer_sql_strings.append(current_outer_sql)
                current_outer_sql = ''
                current_inner_sql = self.LEFT_BRACKET
                left_bracket_counter = left_bracket_counter + 1
            elif char == self.LEFT_BRACKET and left_bracket_counter > 0:
                current_inner_sql = current_inner_sql + char
                left_bracket_counter = left_bracket_counter + 1

            if char  == self.RIGHT_BRACKET and left_bracket_counter > 1:
                current_inner_sql = current_inner_sql + char
                left_bracket_counter = left_bracket_counter - 1
            elif char  == self.RIGHT_BRACKET and left_bracket_counter == 1:
                current_inner_sql += self.RIGHT_BRACKET
                self.inner_sql_strings.append(current_inner_sql)
                current_inner_sql=''
                left_bracket_counter = left_bracket_counter - 1

        # left over string
        if current_outer_sql <> '':
            self.outer_sql_strings.append(current_outer_sql)
            current_outer_sql = ''


    def breakdown_sql_by_set_operators(self):
        # must run after breakdown_sql_by_brackets
        # check if outer sql strings contain SQL_SET_OPERATORS
        # if so need to split them
        sub_sql_counter = 0
        current_inner_sql = ''

        local_inner_sql_strings = []

        for current_outer_string in self.outer_sql_strings:
            current_sqls = re.split(self.SQL_SET_OPERATORS, current_outer_string)

            if len(current_sqls) == 1:
                if len(self.inner_sql_strings) < sub_sql_counter + 1:
                    current_inner_sql += self.outer_sql_strings[sub_sql_counter]
                else:
                    current_inner_sql += self.outer_sql_strings[sub_sql_counter] + \
                                        self.inner_sql_strings[sub_sql_counter]
            else:
                for current_split_sql in current_sqls:
                    if current_inner_sql != '':
                        current_inner_sql += current_split_sql
                        local_inner_sql_strings.append(current_inner_sql)
                        current_inner_sql = ''
                    else:
                        if current_split_sql != current_sqls[-1]:
                            local_inner_sql_strings.append(current_split_sql)
                        else:
                            if len(self.inner_sql_strings) < sub_sql_counter:
                                current_inner_sql = current_split_sql
                            else:
                                current_inner_sql = current_split_sql + \
                                                    self.inner_sql_strings[sub_sql_counter]

            sub_sql_counter += 1

        if len(local_inner_sql_strings) == 0:
            return
        else:
            # left over string
            if current_inner_sql != '':
                local_inner_sql_strings.append(current_inner_sql)
            self.outer_sql_strings = ''
            self.inner_sql_strings = local_inner_sql_strings
