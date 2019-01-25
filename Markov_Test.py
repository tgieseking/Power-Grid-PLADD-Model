from PLADD.Markov import *

tnode0 = TransientNode()
tnode1 = TransientNode()
tnode2 = TransientNode()
anode0 = AbsorbingNode(0)
anode1 = AbsorbingNode(1)

tnode0.set_transitions({tnode0:0.2, tnode1:0.5, tnode2:0.3})
tnode1.set_transitions({anode0: 0.5, anode1:0.5})
tnode2.set_transitions({anode1:1.0})

model = Markov([tnode0, tnode1, tnode2], [anode0, anode1], tnode0)

# import pdb; pdb.set_trace()

# counts = {0:0, 1:1}
# for i in range(1000):
#     counts[model.run_simulation()] += 1
#
# print(counts)

print(model.calculate_output_probs())
