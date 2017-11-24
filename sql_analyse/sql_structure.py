import re

class SqlBlock:
    # static variables
    LEFT_BRACKET = '('
    RIGHT_BRACKET = ')'
    SPACE = ' '

    SQL_SET_OPERATORS = 'union|unionall|minus|intersect'
    SQL_KEY_WORDS = ''

    original_sql_string = ''
    pre_processed_sql_string = ''

    outer_sql_strings = []
    inner_sql_strings = []
    inner_sql_blocks = []

    outer_tables = dict()

    def __init__(self, sql_string):
        self.original_sql_string = sql_string
        self.outer_sql_strings = []
        self.inner_sql_strings = []
        self.inner_sql_blocks = []
        self.initialize_sql_block()

    def initialize_sql_block(self, outer_tables = dict()):

        self.outer_tables = outer_tables

        self.pre_process_sql_block()

        self.breakdown_sql_by_brackets()
        self.breakdown_sql_by_set_operators()

        self.parse_table_name_and_alias()

        for innersql in self.inner_sql_strings:
            inner_sql_block = SqlBlock(innersql)
            inner_sql_block = inner_sql_block.initialize_sql_block(self.outer_tables)
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
        self.pre_processed_sql_string = self.pre_processed_sql_string.replace('union all', 'unionall')

        # add a space before and after comma
        self.pre_processed_sql_string = self.pre_processed_sql_string.replace(',', ' , ')

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

    def parse_table_name_and_alias(self):
        # 1. search from table dictionary
        # 2. use logic to find table name
        # implement 2 first
        TABLE_NAME_START_KEYS = ['from','join']
        TABLE_NAME_SPLIT_KEYS = [',']
        TABLE_NAME_END_KEYS = ['join','where', 'on']

        parse_table_name_flag = False

        table_names = []
        raw_table_name = ''

        for outer_sql_string in self.outer_sql_strings:
            for word in str.split(outer_sql_string):
                if word in TABLE_NAME_START_KEYS:
                    parse_table_name_flag = True
                elif parse_table_name_flag and word not in TABLE_NAME_SPLIT_KEYS:
                    if raw_table_name != '':
                        raw_table_name += ' ' + word
                    else:
                        raw_table_name = word
                elif parse_table_name_flag and word in TABLE_NAME_SPLIT_KEYS:
                    table_names.append(raw_table_name)
                    raw_table_name = ''
                elif parse_table_name_flag and word in TABLE_NAME_END_KEYS:
                    table_names.append(raw_table_name)
                    raw_table_name = ''
                    parse_table_name_flag = False

        # for leftover in raw_table_name add to table names
        if parse_table_name_flag and raw_table_name != '':
            table_names.append(raw_table_name)

        for table_description in table_names:
            table_name = str.split(table_description)[0]

            if len(str.split(table_description)) > 1:
                table_alias = str.split(table_description)[1]
                self.outer_tables[table_alias] = table_name
            else:
                self.outer_tables[table_name] = table_name

    def parse_table_relation(self):
        None