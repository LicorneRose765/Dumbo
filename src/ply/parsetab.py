
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'PROGRAMADD AND ASSIGN CLOSING COMMA DIV DO DOT ENDFOR ENDIF EQ FALSE FOR GT IF IN INTEGER LPAREN LT MUL NE OPENING OR PRINT RPAREN SEMICOLON STRING SUB TRUE TXT VARIABLE\n    BOOLEAN_EXPRESSION : BOOLEAN_EXPRESSION BOOLEAN_OPERATOR BOOLEAN_EXPRESSION\n    \n    MATH_EXPRESSION : MATH_EXPRESSION ADD TERM\n    \n    MATH_EXPRESSION : MATH_EXPRESSION SUB TERM\n    \n    STRING_LIST_INTERIOR : STRING COMMA STRING_LIST_INTERIOR\n    \n    BOOLEAN_EXPRESSION : BOOLEAN\n    \n    MATH_EXPRESSION : TERM\n    \n    STRING_LIST_INTERIOR : STRING\n    \n    BOOLEAN : TRUE\n            | FALSE\n    \n    TERM : TERM MUL FACTOR\n    \n    TERM : TERM DIV FACTOR\n    \n    STRING_LIST : LPAREN STRING_LIST_INTERIOR RPAREN\n    \n    BOOLEAN_OPERATOR : AND\n    \n    TERM : FACTOR\n    \n    EXPRESSION : VARIABLE ASSIGN STRING_EXPRESSION\n               | VARIABLE ASSIGN STRING_LIST\n               | VARIABLE ASSIGN MATH_EXPRESSION\n               | VARIABLE ASSIGN BOOLEAN_EXPRESSION\n    \n    BOOLEAN_OPERATOR : OR\n    \n    FACTOR : INTEGER\n    \n    BOOLEAN_EXPRESSION : MATH_EXPRESSION INTEGER_COMPARATOR MATH_EXPRESSION\n    \n    STRING_EXPRESSION : STRING_EXPRESSION DOT STRING_EXPRESSION\n    \n    STRING_EXPRESSION : STRING\n    \n    INTEGER_COMPARATOR : LT\n                       | GT\n                       | EQ\n                       | NE\n    \n    STRING_EXPRESSION : VARIABLE\n    \n    EXPRESSION : FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR\n    \n    EXPRESSION : FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR\n    \n    EXPRESSION : PRINT STRING_EXPRESSION\n    \n    EXPRESSION : MATH_EXPRESSION\n    \n    EXPRESSION : BOOLEAN_EXPRESSION\n    \n    EXPRESSION : IF_EXPRESSION\n    \n    IF_EXPRESSION : IF BOOLEAN_EXPRESSION DO EXPRESSION_LIST ENDIF\n    \n    EXPRESSION_LIST : EXPRESSION SEMICOLON\n    \n    EXPRESSION_LIST : EXPRESSION SEMICOLON EXPRESSION_LIST\n    \n    DUMBO_BLOCK : OPENING EXPRESSION_LIST CLOSING\n    \n    PROGRAM : DUMBO_BLOCK PROGRAM\n            | TXT PROGRAM\n    \n    PROGRAM : DUMBO_BLOCK\n            | TXT\n    '
    
_lr_action_items = {'TXT':([0,2,3,22,],[3,3,3,-38,]),'OPENING':([0,2,3,22,],[4,4,4,-38,]),'$end':([1,2,3,5,6,22,],[0,-41,-42,-39,-40,-38,]),'VARIABLE':([4,12,13,23,24,53,54,57,66,67,],[9,35,38,9,38,60,38,9,9,9,]),'FOR':([4,23,57,66,67,],[12,12,12,12,12,]),'PRINT':([4,23,57,66,67,],[13,13,13,13,13,]),'IF':([4,23,57,66,67,],[17,17,17,17,17,]),'TRUE':([4,17,23,24,32,33,34,57,66,67,],[19,19,19,19,19,-13,-19,19,19,19,]),'FALSE':([4,17,23,24,32,33,34,57,66,67,],[20,20,20,20,20,-13,-19,20,20,20,]),'INTEGER':([4,17,23,24,25,26,27,28,29,30,31,32,33,34,39,40,57,66,67,],[21,21,21,21,21,21,21,-24,-25,-26,-27,21,-13,-19,21,21,21,21,21,]),'CLOSING':([7,23,43,],[22,-36,-37,]),'SEMICOLON':([8,10,11,14,15,16,18,19,20,21,36,37,38,44,45,46,47,49,50,51,52,55,56,62,64,68,72,73,],[23,-32,-33,-34,-6,-5,-14,-8,-9,-20,-31,-23,-28,-15,-16,-17,-18,-2,-3,-21,-1,-10,-11,-22,-12,-35,-30,-29,]),'ASSIGN':([9,],[24,]),'ADD':([10,15,18,21,42,46,49,50,51,55,56,],[25,-6,-14,-20,25,25,-2,-3,25,-10,-11,]),'SUB':([10,15,18,21,42,46,49,50,51,55,56,],[26,-6,-14,-20,26,26,-2,-3,26,-10,-11,]),'LT':([10,15,18,21,42,46,49,50,55,56,],[28,-6,-14,-20,28,28,-2,-3,-10,-11,]),'GT':([10,15,18,21,42,46,49,50,55,56,],[29,-6,-14,-20,29,29,-2,-3,-10,-11,]),'EQ':([10,15,18,21,42,46,49,50,55,56,],[30,-6,-14,-20,30,30,-2,-3,-10,-11,]),'NE':([10,15,18,21,42,46,49,50,55,56,],[31,-6,-14,-20,31,31,-2,-3,-10,-11,]),'AND':([11,15,16,18,19,20,21,41,47,49,50,51,52,55,56,],[33,-6,-5,-14,-8,-9,-20,33,33,-2,-3,-21,33,-10,-11,]),'OR':([11,15,16,18,19,20,21,41,47,49,50,51,52,55,56,],[34,-6,-5,-14,-8,-9,-20,34,34,-2,-3,-21,34,-10,-11,]),'STRING':([13,24,48,54,65,],[37,37,59,37,59,]),'DO':([15,16,18,19,20,21,41,49,50,51,52,55,56,60,61,64,],[-6,-5,-14,-8,-9,-20,57,-2,-3,-21,-1,-10,-11,66,67,-12,]),'MUL':([15,18,21,49,50,55,56,],[39,-14,-20,39,39,-10,-11,]),'DIV':([15,18,21,49,50,55,56,],[40,-14,-20,40,40,-10,-11,]),'ENDIF':([23,43,63,],[-36,-37,68,]),'ENDFOR':([23,43,70,71,],[-36,-37,72,73,]),'LPAREN':([24,53,],[48,48,]),'IN':([35,],[53,]),'DOT':([36,37,38,44,62,],[54,-23,-28,54,54,]),'RPAREN':([58,59,69,],[64,-7,-4,]),'COMMA':([59,],[65,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'PROGRAM':([0,2,3,],[1,5,6,]),'DUMBO_BLOCK':([0,2,3,],[2,2,2,]),'EXPRESSION_LIST':([4,23,57,66,67,],[7,43,63,70,71,]),'EXPRESSION':([4,23,57,66,67,],[8,8,8,8,8,]),'MATH_EXPRESSION':([4,17,23,24,27,32,57,66,67,],[10,42,10,46,51,42,10,10,10,]),'BOOLEAN_EXPRESSION':([4,17,23,24,32,57,66,67,],[11,41,11,47,52,11,11,11,]),'IF_EXPRESSION':([4,23,57,66,67,],[14,14,14,14,14,]),'TERM':([4,17,23,24,25,26,27,32,57,66,67,],[15,15,15,15,49,50,15,15,15,15,15,]),'BOOLEAN':([4,17,23,24,32,57,66,67,],[16,16,16,16,16,16,16,16,]),'FACTOR':([4,17,23,24,25,26,27,32,39,40,57,66,67,],[18,18,18,18,18,18,18,18,55,56,18,18,18,]),'INTEGER_COMPARATOR':([10,42,46,],[27,27,27,]),'BOOLEAN_OPERATOR':([11,41,47,52,],[32,32,32,32,]),'STRING_EXPRESSION':([13,24,54,],[36,44,62,]),'STRING_LIST':([24,53,],[45,61,]),'STRING_LIST_INTERIOR':([48,65,],[58,69,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> PROGRAM","S'",1,None,None,None),
  ('BOOLEAN_EXPRESSION -> BOOLEAN_EXPRESSION BOOLEAN_OPERATOR BOOLEAN_EXPRESSION','BOOLEAN_EXPRESSION',3,'p_booleanexpression','bool.py',10),
  ('MATH_EXPRESSION -> MATH_EXPRESSION ADD TERM','MATH_EXPRESSION',3,'p_mathexpression_plus','math.py',10),
  ('MATH_EXPRESSION -> MATH_EXPRESSION SUB TERM','MATH_EXPRESSION',3,'p_mathexpression_minus','math.py',17),
  ('STRING_LIST_INTERIOR -> STRING COMMA STRING_LIST_INTERIOR','STRING_LIST_INTERIOR',3,'p_stringlistinterior_double','base.py',19),
  ('BOOLEAN_EXPRESSION -> BOOLEAN','BOOLEAN_EXPRESSION',1,'p_booleanexpression_simple','bool.py',22),
  ('MATH_EXPRESSION -> TERM','MATH_EXPRESSION',1,'p_mathexpression_TERM','math.py',24),
  ('STRING_LIST_INTERIOR -> STRING','STRING_LIST_INTERIOR',1,'p_stringlistinterior_single','base.py',30),
  ('BOOLEAN -> TRUE','BOOLEAN',1,'p_boolean','bool.py',31),
  ('BOOLEAN -> FALSE','BOOLEAN',1,'p_boolean','bool.py',32),
  ('TERM -> TERM MUL FACTOR','TERM',3,'p_term_times','math.py',31),
  ('TERM -> TERM DIV FACTOR','TERM',3,'p_term_div','math.py',38),
  ('STRING_LIST -> LPAREN STRING_LIST_INTERIOR RPAREN','STRING_LIST',3,'p_stringlist','base.py',39),
  ('BOOLEAN_OPERATOR -> AND','BOOLEAN_OPERATOR',1,'p_booleanoperator_and','bool.py',41),
  ('TERM -> FACTOR','TERM',1,'p_term_factor','math.py',45),
  ('EXPRESSION -> VARIABLE ASSIGN STRING_EXPRESSION','EXPRESSION',3,'p_expression_assignments','base.py',48),
  ('EXPRESSION -> VARIABLE ASSIGN STRING_LIST','EXPRESSION',3,'p_expression_assignments','base.py',49),
  ('EXPRESSION -> VARIABLE ASSIGN MATH_EXPRESSION','EXPRESSION',3,'p_expression_assignments','base.py',50),
  ('EXPRESSION -> VARIABLE ASSIGN BOOLEAN_EXPRESSION','EXPRESSION',3,'p_expression_assignments','base.py',51),
  ('BOOLEAN_OPERATOR -> OR','BOOLEAN_OPERATOR',1,'p_booleanoperator_or','bool.py',50),
  ('FACTOR -> INTEGER','FACTOR',1,'p_factor_num','math.py',52),
  ('BOOLEAN_EXPRESSION -> MATH_EXPRESSION INTEGER_COMPARATOR MATH_EXPRESSION','BOOLEAN_EXPRESSION',3,'p_integercomparison','bool.py',59),
  ('STRING_EXPRESSION -> STRING_EXPRESSION DOT STRING_EXPRESSION','STRING_EXPRESSION',3,'p_stringexpression_double','base.py',62),
  ('STRING_EXPRESSION -> STRING','STRING_EXPRESSION',1,'p_string_expression_string','base.py',71),
  ('INTEGER_COMPARATOR -> LT','INTEGER_COMPARATOR',1,'p_integercomparator','bool.py',71),
  ('INTEGER_COMPARATOR -> GT','INTEGER_COMPARATOR',1,'p_integercomparator','bool.py',72),
  ('INTEGER_COMPARATOR -> EQ','INTEGER_COMPARATOR',1,'p_integercomparator','bool.py',73),
  ('INTEGER_COMPARATOR -> NE','INTEGER_COMPARATOR',1,'p_integercomparator','bool.py',74),
  ('STRING_EXPRESSION -> VARIABLE','STRING_EXPRESSION',1,'p_string_expression_variable','base.py',80),
  ('EXPRESSION -> FOR VARIABLE IN STRING_LIST DO EXPRESSION_LIST ENDFOR','EXPRESSION',7,'p_expression_strlistfor','base.py',97),
  ('EXPRESSION -> FOR VARIABLE IN VARIABLE DO EXPRESSION_LIST ENDFOR','EXPRESSION',7,'p_expression_varfor','base.py',111),
  ('EXPRESSION -> PRINT STRING_EXPRESSION','EXPRESSION',2,'p_expression_print','base.py',128),
  ('EXPRESSION -> MATH_EXPRESSION','EXPRESSION',1,'p_expression_mathexpression','base.py',137),
  ('EXPRESSION -> BOOLEAN_EXPRESSION','EXPRESSION',1,'p_expression_booleanexpression','base.py',146),
  ('EXPRESSION -> IF_EXPRESSION','EXPRESSION',1,'p_expression_ifexpression','base.py',155),
  ('IF_EXPRESSION -> IF BOOLEAN_EXPRESSION DO EXPRESSION_LIST ENDIF','IF_EXPRESSION',5,'p_ifexpression','base.py',164),
  ('EXPRESSION_LIST -> EXPRESSION SEMICOLON','EXPRESSION_LIST',2,'p_expression_list_single','base.py',176),
  ('EXPRESSION_LIST -> EXPRESSION SEMICOLON EXPRESSION_LIST','EXPRESSION_LIST',3,'p_expression_list_multiple','base.py',185),
  ('DUMBO_BLOCK -> OPENING EXPRESSION_LIST CLOSING','DUMBO_BLOCK',3,'p_dumboblock','base.py',194),
  ('PROGRAM -> DUMBO_BLOCK PROGRAM','PROGRAM',2,'p_program_double','base.py',203),
  ('PROGRAM -> TXT PROGRAM','PROGRAM',2,'p_program_double','base.py',204),
  ('PROGRAM -> DUMBO_BLOCK','PROGRAM',1,'p_program_single','base.py',213),
  ('PROGRAM -> TXT','PROGRAM',1,'p_program_single','base.py',214),
]
