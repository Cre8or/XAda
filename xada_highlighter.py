"""X-tended Ada Syntax Highlighter

This plugin provides extended syntax highlighting for Ada source files.
It also adds additional highlighting styles, which can be reconfigured
inside the GNAT preferences (under "Editor" > "Fonts & Colours").

Copyright (C) 2021-2023 Cre8or
"""

import sys
sys.path.append("/xada_lib")

# IMPORTS
import GPS
from xada_lib.common import *
from highlighter.engine import Style

from gi.repository import Gtk, GLib, Gdk, Pango
from pygps import get_gtk_buffer, is_editor_visible

import theme_handling
from theme_handling import Color, transparent





# --------------------------------------------------------------------------------------------------------------------------------
# Language-specific definitions
# --------------------------------------------------------------------------------------------------------------------------------

ada_attributes = r"(?<=\')" + ("|" + r"(?<=\')").join([
	"Abort_Signal",
	"Access",
	"Address",
	"Address_Size",
	"Adjacent",
	"Aft",
	"Alignment",

	"Base",
	"Bit",
	"Bit_Order",
	"Bit_Position",
	"Body_Version",

	"Callable",
	"Caller",
	"Ceiling",
	"Class",
	"Code_Address",
	"Compiler_Version",
	"Component_Size",
	"Compose",
	"Constrained",
	"Copy_Sign",
	"Count",

	"Default_Bit_Order",
	"Default_Scalar_Storage_Order",
	"Definite",
	"Delta",
	"Denorm",
	"Deref",
	"Descriptor_Size",
	"Digits",

	"Elab_Body",
	"Elab_Spec",
	"Elab_Subp_Body",
	"Elaborated",
	"Emax",
	"Enabled",
	"Enum_Rep",
	"Enum_Val",
	"Epsilon",
	"Exponent",
	"External_Tag",

	"Fast_Math",
	"Finalization_Size",
	"First",
	"First_Bit",
	"First_Valid",
	"Fixed_Value",
	"Floor",
	"Fore",
	"Fraction",
	"From_Any",

	"Has_Access_Values",
	"Has_Discriminants",
	"Has_Same_Storage",

	"Identity",
	"Image",
	"Img",
	"Input",
	"Integer_Value",
	"Invalid_Value",
	"Iterable",

	"Large",
	"Last",
	"Last_Bit",
	"Last_Valid",
	"Leading_Part",
	"Length",
	"Library_Level",
	"Lock_Free",
	"Loop_Entry",

	"Machine",
	"Machine_Emax",
	"Machine_Emin",
	"Machine_Mantissa",
	"Machine_Overflows",
	"Machine_Radix",
	"Machine_Rounding",
	"Machine_Rounds",
	"Machine_Size",
	"Mantissa",
	"Max",
	"Max_Alignment_For_Allocation",
	"Max_Size_In_Storage_Elements",
	"Maximum_Alignment",
	"Mechanism_Code",
	"Min",
	"Mod",
	"Model",
	"Model_Emin",
	"Model_Epsilon",
	"Model_Mantissa",
	"Model_Small",
	"Modulus",

	"Null_Parameter",

	"Object_Size",
	"Old",
	"Output",
	"Overlaps_Storage",

	"Partition_Id",
	"Passed_By_Reference",
	"Pool_Address",
	"Pos",
	"Position",
	"Pred",
	"Priority",

	"Range",
	"Range_Length",
	"Read",
	"Remainder",
	"Restriction_Set",
	"Result",
	"Round",
	"Rounding",

	"Safe_Emax",
	"Safe_First",
	"Safe_Large",
	"Safe_Last",
	"Safe_Small",
	"Scalar_Storage_Order",
	"Scale",
	"Scaling",
	"Signed_Zeros",
	"Simple_Storage_Pool",
	"Size",
	"Small",
	"Storage_Pool",
	"Storage_Size",
	"Storage_Unit",
	"Stream_Size",
	"Stub_Type",
	"Succ",
	"System_Allocator_Alignment",

	"Tag",
	"Target_Name",
	"Terminated",
	"To_Address",
	"To_Any",
	"Truncation",
	"Type_Class",
	"Type_Key",
	"TypeCode",

	"Unbiased_Rounding",
	"Unchecked_Access",
	"Unconstrained_Array",
	"Universal_Literal_String",
	"Unrestricted_Access",
	"Update",

	"VADS_Size",
	"Val",
	"Valid",
	"Valid_Scalars",
	"Value",
	"Value_Size",
	"Version",

	"Wchar_T_Size",
	"Wide_Image",
	"Wide_Value",
	"Wide_Wide_Image",
	"Wide_Wide_Value",
	"Wide_Wide_Width",
	"Wide_Width",
	"Width",
	"Word_Size",
	"Write",

	# GNAT Preprocessor
	"Defined",
])

ada_keywords = "|".join([
	"abort",
	"abs",
	"abstract",
	"accept",
	"access",
	"aliased",
	"all",
	"and",
	"array",
	"at",

	"begin",
	"body",

	"case",
	"constant",

	"declare",
	"delay",
	"delta",
	"digits",
	"do",

	"else",
	"elsif",
	"end",
	"entry",
	"exception",
	"exit",

	"for",
	"function",

	"generic",
	"goto",

	"if",
	"in",
	"interface",
	"is",

	"limited",
	"loop",

	"mod",

	"new",
	"not",
	"null",

	"of",
	"or",
	"others",
	"out",
	"overriding",

	"package",
	"pragma",
	"private",
	"procedure",
	"protected",

	"raise",
	"range",
	"record",
	"rem",
	"renames",
	"return",
	"reverse",

	"select",
	"separate",
	"subtype",
	"synchronized",

	"tagged",
	"task",
	"terminate",
	"then",
	"type",

	"until",
	"use",

	"when",
	"while",
	"with",

	"xor",
])

ada_predefined_types = "|".join([
	# Standard
	"Boolean",

	"Character",

	"Duration",

	"Float",

	"Integer",

	"Long_Float",
	"Long_Integer",
	"Long_Long_Float",
	"Long_Long_Integer",

	"Natural",

	"Positive",

	"String",

	"Wide_Character",
	"Wide_String",
	"Wide_Wide_Character",
	"Wide_Wide_String",

	# Interfaces
	"IEEE_Extended_Float",
	"IEEE_Float_32",
	"IEEE_Float_64",
	"Integer_8",
	"Integer_16",
	"Integer_24",
	"Integer_32",
	"Integer_64",

	"Unsigned_8",
	"Unsigned_16",
	"Unsigned_24",
	"Unsigned_32",
	"Unsigned_64",
])

ada_predefined_exceptions = "|".join([
	# Standard
	"Constraint_Error",

	"Program_Error",

	"Storage_Error",

	"Tasking_Error",

	# IO_Exceptions
	"Data_Error",
	"Device_Error",

	"End_Error",

	"Layout_Error",

	"Mode_Error",

	"Name_Error",

	"Status_Error",

	"Use_Error",
])

ada_predefined_enumerations = "|".join([
	"false",

	"true",
])

ada_predefined_packages = "|".join([
	# Standard
	"Ada",

	"ASCII",

	"Directories",

	"Interfaces",
	"IO_Exceptions",

	"Numerics",

	"OS_Lib",

	"Real_Time",

	"Stream_IO",

	"Text_IO",

	# OpenGL
	"GL",
	"Glfw",
	"Dear_ImGui",

	# Custom (NOTE: add user/application-specific units here)
	"A3D",
])





# --------------------------------------------------------------------------------------------------------------------------------
# Base definitions
# --------------------------------------------------------------------------------------------------------------------------------

def_identifier = r"[a-zA-Z][a-zA-Z0-9]*(?:_[a-zA-Z0-9]+)*"
def_number = r"\b[0-9]+(?:_[0-9]+)*(?:\.[0-9]+)?(?:_[0-9]+)*"
def_number_based = r"\b[0-9]+#[0-9a-f]+(?:_[0-9a-f]+)*#"
def_character = r"\'.\'"

def_escape_identifier = r"(?<![a-zA-Z0-9_])"

def_negative_lookahead_blocks = "(?!(?:" + "\s+)|(?:".join([
	"begin",

	"declare",

	"for",

	"loop",

	"while",
]) + "\s+))"

def_preprocessor = def_escape_identifier + r"#[a-zA-Z0-9_]+\b"

def_include_string = r"(?<=#include[ \t])[ \t]*<[^\n\r>]+>"
def_class_cpp = def_escape_identifier + def_identifier + r"(?=::)"





# --------------------------------------------------------------------------------------------------------------------------------
# Custom definitions
# --------------------------------------------------------------------------------------------------------------------------------

custom_types = def_escape_identifier + r"t(?:_[a-z0-9]+)+"

custom_enumeration = def_escape_identifier + r"e(?:_[a-z0-9]+)+"

custom_constants = def_escape_identifier + r"c(?:_[a-z0-9]+)+"

custom_packages = def_escape_identifier + r"p(?:_[a-z0-9]+)+"

custom_members = def_escape_identifier + r"[mg](?:_[a-z0-9]+)+"

custom_exceptions_prefix = def_escape_identifier + r"ex(?:_[a-z0-9]+)+"
custom_exceptions_suffix = def_identifier + "_exception" + r"(?![a-z0-9_])"

custom_macros = r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\b"




# --------------------------------------------------------------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------------------------------------------------------------

tag_attribute = new_style(
	lang="Ada",
	name="ada_attribute",
	label="Attributes",
	doc="Any standard attribute of a type, or of an object.",
	foreground_colors=("#93FFFF", "#93FFFF")
)

tag_exception = new_style(
	lang="Ada",
	name="ada_exception",
	label="Exceptions",
	doc="Any identifier starting with \"EX_\" or ending with \"_EXCEPTION\". Includes standard exceptions.",
	font_style="bold",
	foreground_colors=("#FF3D3D", "#FF3D3D")
)

tag_enumeration = new_style(
	lang="Ada",
	name="ada_enumeration",
	label="Enumerations",
	doc="Any identifier starting with \"E_\". Includes standard booleans.",
	font_style="bold",
	foreground_colors=("#FFB3D7", "#FFB3D7")
)

tag_constant = new_style(
	lang="Ada",
	name="ada_constant",
	label="Constants",
	doc="Any identifier starting with \"C_\".",
	foreground_colors=("#F9C0B3", "#F9C0B3")
)

tag_package = new_style(
	lang="Ada",
	name="ada_package",
	label="Packages",
	doc="Any identifier starting with \"P_\".",
	foreground_colors=("#5BC2B0", "#5BC2B0")
)

tag_pragma = new_style(
	lang="Ada",
	name="ada_pragma",
	label="Pragmas",
	doc="Any identifier following the keyword \"pragma\".",
	foreground_colors=("#44B6FF", "#44B6FF")
)

tag_operator = new_style(
	lang="Ada",
	name="ada_operator",
	label="Operators",
	doc="Any operator or special character: ()+-*/:=,.;\'>",
	font_style="bold",
	foreground_colors=("#FFEF70", "#FFEF70"),
	prio=2
)

tag_member = new_style(
	lang="Ada",
	name="ada_member",
	label="Members",
	doc="Any identifier starting with \"m_\" or \"G_\". Used for member variables of classes, or global variables.",
	foreground_colors=("#E8DCB3", "#E8DCB3"),
	prio=2
)

# Hack to duplicate the keyword tag, but with higher priority
tag_keyword_prio = Style("keyword_prio", 4, tag_keyword.pref)





# --------------------------------------------------------------------------------------------------------------------------------
# Highlighters
# --------------------------------------------------------------------------------------------------------------------------------

hl_string = region('"', r'"|[^\\]$', matchall=False, tag=tag_string)

hl_operator = simple(r"[\(\)\+\-\*\/\:\&\=\,\.\;\'\<\>\{\}]", tag_operator)

hl_comment = region(
	r"--",
	r"[\n\r]",
	igncase=False,
	tag=tag_comment,
	highlighter=(
		simple(r"TO-?DO(?![a-zA-Z0-9_])", tag_annotation),
		simple(r"DEBUG(?![a-zA-Z0-9_])", tag_annotation),
	)
)

hl_comment_cpp_single = region(
	r"\/\/",
	r"[\n\r]",
	igncase=False,
	tag=tag_comment,
	highlighter=(
		simple(r"TO-?DO(?![a-zA-Z0-9_])", tag_annotation),
		simple(r"DEBUG(?![a-zA-Z0-9_])", tag_annotation),
	)
)

hl_comment_cpp_multi = region(
	r"\/\*",
	r"\*\/",
	igncase=False,
	tag=tag_comment,
	highlighter=(
		simple(r"TO-?DO(?![a-zA-Z0-9_])", tag_annotation),
		simple(r"DEBUG(?![a-zA-Z0-9_])", tag_annotation),
	)
)

hl_identifier_declaration = region(
	r"(?<=\:)\s*(?=[a-z])" + def_negative_lookahead_blocks,
	r"(?!(?:_?[a-z0-9])+|(?:\s+(?!(?:renames)|(?:with)|(?:do)\s+)))",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		words(ada_keywords, tag=tag_keyword_prio),
		simple(def_identifier, tag_type),
		simple(r"\.", tag_operator),
	)
)

hl_package_body = region(
	r"(?<![a-z0-9_])body\s+",
	r"(?<![^a-z0-9_]body)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		simple(def_identifier, tag_block),
		simple(r"\.", tag_operator),
	)
)

hl_package = region(
	r"(?<![a-z0-9_])package\s+(?!body\s+)",
	r"(?<![^a-z0-9_]package)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		simple(def_identifier, tag_block),
		simple(r"\.", tag_operator),
	)
)

hl_procedure = region(
	r"(?<![a-z0-9_])procedure\s+",
	r"(?<![^a-z0-9_]procedure)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		simple(def_identifier, tag_block),
	)
)

hl_function_return = region(
	r"\s+return\s+",
	r"(?<![^a-z0-9_](?:(?:.{2}\sreturn)|(?:.{5}\snot)|(?:.{4}\snull)|(?:.{2}\saccess)|(?:\sconstant)))",	# Look-behind requires fixed-width patterns in GNAT Studio
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		words(ada_keywords, tag=tag_keyword_prio),
		simple(def_identifier, tag_type),
		simple(r"\.", tag_operator),
	)
)

hl_function_parentheses = region(
	r"[ \t]*\(",
	r"\)",
	name="hl_function_parentheses",
	igncase=True,
	tag=tag_operator,
	highlighter=(
		# Comments
		hl_comment,

		# Attributes
		words(ada_attributes, tag=tag_attribute),

		# Keywords
		words(ada_keywords, tag=tag_keyword_prio),

		# Literals
		simple(def_number_based, tag_number),
		simple(def_number, tag_number),
		simple(def_character, tag_string),
		hl_string,

		# Types
		hl_identifier_declaration,
		words(ada_predefined_types, tag=tag_type),
		simple(custom_types, tag_type),

		# Enumerations
		words(ada_predefined_enumerations, tag=tag_enumeration),
		simple(custom_enumeration, tag_enumeration),

		# Constants
		simple(custom_constants, tag_constant),

		# Packages
		words(ada_predefined_packages, tag=tag_package),
		simple(custom_packages, tag_package),

		# Members
		simple(custom_members, tag_member),

		# Operators (excluding parentheses)
		simple(r"[\+\-\*\/\:\&\=\,\.\;\'\<\>]", tag_operator),

		# Recursion
		region_ref("hl_function_parentheses"),

		# Identifiers
		simple(def_identifier, tag_default),
	)
)

hl_function = region(
	r"(?<![a-z0-9_])function\s+",
	r"(?<![^a-z0-9_]function)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		# Operator functions ("+", "-", "mod", "xor", etc.)
		region('"', r'"|[^\\]$', matchall=False, tag=tag_block),

		simple(def_identifier, tag_block),

		hl_function_parentheses,

		hl_function_return,
	)
)

hl_entry = region(
	r"(?<![a-z0-9_])entry\s+",
	r"(?<![^a-z0-9_]entry)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		simple(def_identifier, tag_block),
	)
)

hl_accept = region(
	r"(?<![a-z0-9_])accept\s+",
	r"(?<![^a-z0-9_]accept)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		simple(def_identifier, tag_block),
	)
)

hl_block_end = region(
	r"(?<![a-z0-9_])end\s+",
	r"(?<![^a-z0-9_]end)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		words(ada_keywords, tag=tag_keyword),
		simple(def_identifier, tag_block),
		simple(r"\.", tag_operator),
	)
)

hl_case_block = region(
	r"(?<=[^a-z0-9])when(?=\s+[a-z0-9_]+\s*\:\s*.+(?:.\|\s)*=>)",
	r"(?==>)",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		# Keywords
		words(ada_keywords, tag=tag_keyword),

		# Exceptions
		words(ada_predefined_exceptions, tag=tag_exception),
		simple(custom_exceptions_prefix, tag_exception),
		simple(custom_exceptions_suffix, tag_exception),

		# Packages
		words(ada_predefined_packages, tag=tag_package),
		simple(custom_packages, tag_package),

		# Members
		simple(custom_members, tag_member),

		# Operators
		simple(r"[\.\:\|\(\)]", tag_operator),

		# Identifiers
		simple(def_identifier, tag_default),
	)
)

hl_use_type = region(
	r"(?<![a-z0-9_])use\s+type\s+",
	r"(?=[;\s\n])",
	igncase=True,
	tag=tag_keyword,
	highlighter=(
		words(ada_keywords, tag=tag_keyword_prio),
		simple(def_identifier, tag_type),
		simple(r"\.", tag_operator),
	)
)





# --------------------------------------------------------------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------------------------------------------------------------

register_highlighter(
	language="ada",
	spec=(
		# Comments
		hl_comment,

		# Priority highlighters
		hl_package_body,
		hl_package,
		hl_procedure,
		hl_function,
		hl_entry,
		hl_accept,
		hl_block_end,
		hl_case_block,
		hl_use_type,

		# Attributes
		words(ada_attributes, tag=tag_attribute),

		# Keywords
		words(ada_keywords, tag=tag_keyword),

		# Literals
		simple(def_number_based, tag_number),
		simple(def_number, tag_number),
		simple(def_character, tag_string),
		hl_string,

		# Types
		hl_identifier_declaration,
		words(ada_predefined_types, tag=tag_type),
		simple(custom_types, tag_type),

		# Exceptions
		words(ada_predefined_exceptions, tag=tag_exception),
		simple(custom_exceptions_prefix, tag_exception),
		simple(custom_exceptions_suffix, tag_exception),

		# Enumerations
		words(ada_predefined_enumerations, tag=tag_enumeration),
		simple(custom_enumeration, tag_enumeration),

		# Constants
		simple(custom_constants, tag_constant),

		# Packages
		words(ada_predefined_packages, tag=tag_package),
		simple(custom_packages, tag_package),

		# Members
		simple(custom_members, tag_member),

		# Pragmas
		simple(r"(?<=pragma)[\t ]+" + def_identifier, tag_pragma),

		# Operators
		hl_operator,
	),
	igncase=True
)


register_highlighter(
	language="c++",
	spec=(
		# Comments
		hl_comment_cpp_multi,
		hl_comment_cpp_single,

		# Literals
		simple(def_number_based, tag_number),
		simple(def_number, tag_number),
		simple(def_character, tag_string),
		simple(def_include_string, tag_string),
		hl_string,

		# Preprocessor directives
		simple(def_preprocessor, tag_preprocessor),

		# C++ classes
		simple(def_class_cpp, tag_package),

		# Enumerations
		words(ada_predefined_enumerations, tag=tag_enumeration),
		simple(custom_enumeration, tag_enumeration),
		simple(custom_macros, tag_enumeration),

		# Constants
		simple(custom_constants, tag_constant),

		# Members
		simple(custom_members, tag_member),

		# Operators
		hl_operator,
	),
	igncase=False
)
