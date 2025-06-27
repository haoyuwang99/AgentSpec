import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/../../../../')
from parser.ast import ASTDumper,Parse
if __name__ == "__main__":
	assert len(sys.argv)==2
	ast=Parse(sys.argv[1])
	dumper=ASTDumper(ast)
	dumper.dump()
	