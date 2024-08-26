import matplotlib.pyplot as plt
import numpy as np
import os

log_file_path = r'C:\Users\BharathKumar_Bellam\osgenai-code-generator\job_log.txt'

def log(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

try:
    log("Job started")
    x = np.linspace(1, 5, 11)
    y = x ** 2
    plt.plot(x, y, 'r')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('Practice plot')
    plot_file_path = r'C:\Users\BharathKumar_Bellam\osgenai-code-generator\practice_plot.png'
    plt.savefig(plot_file_path)  # Save the plot to a file
    log(f"Job completed and plot saved to {plot_file_path}")
except Exception as e:
    log(f"Error: {str(e)}")
