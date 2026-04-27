# main.py

from graphbuilder import build_graph

if __name__ == "__main__":

    graph = build_graph()
    graph_obj = graph.get_graph()

    print(graph_obj.draw_mermaid())
    result = graph.invoke({})

    print("\nFINAL RESULT\n")

    print(result["final_prior_auth"])