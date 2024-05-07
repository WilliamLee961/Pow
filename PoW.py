import random
from matplotlib import pyplot as plt


class BlockchainSimulation:
    def __init__(self, node_count, malicious_node_ratio, success_rate):
        self.node_count = node_count
        self.malicious_node_ratio = malicious_node_ratio
        self.malicious_node_count = int(node_count * malicious_node_ratio)
        self.success_rate = success_rate
        self.chain_length = 0
    
    def simulate_round(self):
        # 在同步网络中，认为每个节点进行一次计算，且节点在一轮中得到一个以上块的概率很小，用数字来区分是否得到块，块持有者为正常还是恶意节点
        # 2 表示最终没得到块， 1表示恶意节点持有块 0表示诚实节点持有块
        for i in range(self.node_count):
            # random.random 取值范围：闭区间0到开区间1
            if random.random() < self.success_rate:
                if i < self.malicious_node_count:
                    return 1
                else:
                    return 0
        return 2
    
    def simulate_attack(self, attack_rounds=100, target_fork_length=6):
        # 模拟1000轮次内的六个块分叉攻击，如果在1000轮以内生成了一个六个块的分叉认为恶意节点分叉成功
        honest_chain = 0
        malicious_chain = 0
        for _ in range(attack_rounds):
            # 这里忽略success rate，我们只想观察分叉攻击成功率和恶意节点比例的关系，如果加上success rate那么很多轮不出节点，
            # 需要我们大大增加攻击轮次， 消耗时间空间， 我们这里只是模拟，所以省略
            if random.random() < self.malicious_node_ratio:
                malicious_chain += 1
            else:
                honest_chain += 1
            if malicious_chain < honest_chain:
                honest_chain = 0
                malicious_chain = 0
            if malicious_chain == honest_chain + target_fork_length:
                return True
        return False
    
    def simulate_selfish_mining(self, rounds=1000):
        # 模拟自私挖矿，计算收益比例(1000rounds这里表示1000个恶意节点持有块之后的那个轮次)
        profits = 0
        for _ in range(rounds):
            if random.random() < self.malicious_node_ratio:
                profits += 2
            else:
                if random.random() < 0.5:
                    profits += 1
        # 基础收益每个rounds都是1，gain除以rounds得到自私挖矿的额外收益比例
        return profits/rounds


    def run_simulation(self, rounds=1000, attack_rounds=1000):
        # 主模拟过程
        blocks = []

        # 测量区块链增长速度(用每个轮次出块数量定义)并记录节点恶意与否：
        for _ in range(rounds):
            block = self.simulate_round()
            if block == 1:
                blocks.append("malicious")
            elif block == 0:
                blocks.append("honest")

        self.chain_length = len(blocks)
        growth_rates = self.chain_length/rounds

        # 实现长度为6的分叉攻击
        success_attacks = 0
        target_fork_length = 6

        for _ in range(rounds):
            if self.simulate_attack(attack_rounds, target_fork_length):
                success_attacks += 1

        success_attack_ratio = success_attacks/rounds
        selfish_mining_profits = self.simulate_selfish_mining()
        
        return growth_rates, success_attack_ratio, selfish_mining_profits

node_count = 100
success_rate_list = [5e-4,1e-3,5e-3,1e-2]
malicious_node_ratio = 0.1
growth_rates_list = []
for success_rate in success_rate_list:
    simulation = BlockchainSimulation(node_count, malicious_node_ratio, success_rate)
    growth_rates, _, _ = simulation.run_simulation()
    growth_rates_list.append(growth_rates)

# 可视化区块链增长速度随出块成功率
plt.figure(figsize=(10,6))
plt.plot(success_rate_list, growth_rates_list, marker='o')
plt.title('Blockchain Growth Rates')
plt.xlabel('Success Rates')
plt.ylabel('Blockchain Growth Rates')
plt.grid(True)
plt.show()


node_count = 100
malicious_node_ratios = [0.1,0.2,0.3,0.4,0.5]
success_rate = 0.001
growth_rates_list = []
success_attack_ratio_list = []
selfish_mining_profits_list = []

for malicious_node_ratio in malicious_node_ratios:
    simulation = BlockchainSimulation(node_count, malicious_node_ratio, success_rate)
    growth_rates, success_attack_ratio, selfish_mining_profits = simulation.run_simulation(attack_rounds=1000)
    growth_rates_list.append(growth_rates)
    success_attack_ratio_list.append(success_attack_ratio)
    selfish_mining_profits_list.append(selfish_mining_profits)

    print("恶意节点比例：",malicious_node_ratio)
    print("区块链增长速度:", growth_rates)
    print("分叉攻击成功概率:", success_attack_ratio)
    print("自私挖矿收益比例:", selfish_mining_profits)

# 可视化分叉攻击成功率随恶意节点比例的变化
plt.figure(figsize=(10,6))
plt.plot(malicious_node_ratios, success_attack_ratio_list, marker='o')
plt.title('Success Attack Ratio')
plt.xlabel('Malicious Node Ratio')
plt.ylabel('Success Attack Ratio')
plt.grid(True)
plt.show()

# 可视化自私挖矿收益随恶意节点比例的变化
plt.figure(figsize=(10,6))
plt.plot(malicious_node_ratios, selfish_mining_profits_list, marker='o')
plt.title('Selfish Mining Profits Ratio')
plt.xlabel('Malicious Node Ratio')
plt.ylabel('Selfish Mining Profits Ratio')
plt.grid(True)
plt.show()
