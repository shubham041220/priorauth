# main.py

from graphbuilder import build_graph

if __name__ == "__main__":

    graph = build_graph()

    result = graph.invoke({})

    print("\nFINAL RESULT\n")

    print(result["final_prior_auth"])