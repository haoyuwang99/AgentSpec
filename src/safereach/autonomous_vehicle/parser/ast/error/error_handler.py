################################################################################################################
#  Default error handler:
# 1.When raise an UndefinedVariableError:
# filename:line:column:error: use of undeclared identifier 'var'
# 	some content
#
# 2.When raise a RedefinitionVariableError:
# filename:line:column:error: redefinition of 'var'
#	some content
#
# 3.When raise an IllegalTypeError:
# filename:line:column:
# 	error: illegal type '<class var_type>' of 'var', expecting '<class true_type>'
#	some content
#
# 4.WeatherContinuousIndexFormatError:
# filename:line:column:
# 	error:"id" illegal weather continuous index format,weather continuous index must be 0.0-1.0
# 	some content
#
# 5.IntersectionIDFormatError:
# filename:line:column:
# 	error:"id" illegal intersection id format,intersection id must be integer
#	some content

# 6.LaneFormatError:
# filename:line:column:error:"lane_id" illegal lane id format,lane id string must be consisting real number'
# 	some content
# 7.
################################################################################################################
try:
	from rich.console import Console
	#TODO:Colorful printing
	console=Console(stderr=True,color_system="standard")
except:
	pass
import sys
from parser.ast.error.error import *
def set_error_handler(e:BasicError,file_name:AnyStr):
	'''
	set_error_handler works when getting a predefined error.
	:param e: base error
	"param file_name: the source file where e occurs
	'''
	if isinstance(e,BasicError):
		sys.stderr.write(f'{file_name}:{str(e)}\n')