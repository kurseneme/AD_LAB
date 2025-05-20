import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy import signal


start_amplitude = 1.0
start_frequency = 1.0
start_phase = 0.0
start_noise_mean = 0.0
start_noise_std = 0.1
start_guassian_sigma = 1.0

time = np.linspace(0, 2 * np.pi, 1000)
noise = np.random.normal(start_noise_mean, start_noise_std, size=time.shape)


def generate_harmonic(time, amplitude, frequency, phase, noise, show_noise):
    harmonic = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    if show_noise:
        return harmonic + noise
    else:
        return harmonic


def apply_gaussian(harmonic, sigma):
    window = signal.windows.gaussian(len(harmonic), sigma)
    guassian = signal.convolve(harmonic, window/window.sum(), mode='same')
    return guassian


def update_plots(val=None):
    amplitude = amplitude_slider.val
    frequency = frequency_slider.val
    phase = phase_slider.val
    show_noise = noise_butt.get_status()[0]
    sigma = gauss_sigma_slider.val

    raw = generate_harmonic(time, amplitude, frequency, phase, noise, show_noise)
    filtered = apply_gaussian(raw, sigma)

    plot_raw.set_ydata(raw)
    plot_filtered.set_ydata(filtered)
    plot_raw.figure.canvas.draw_idle()


def update_noise(val):
    global noise
    noise = np.random.normal(noise_mean_slider.val, noise_std_slider.val, size=time.shape)
    update_plots()


def reset_all(event):
    amplitude_slider.reset()
    frequency_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_std_slider.reset()
    gauss_sigma_slider.reset()
    if noise_butt.get_status()[0] != True:
        noise_butt.set_active(0)
    update_plots()


fig = plt.figure(figsize=(12, 8))
ax_amplitude = plt.axes([0.12, 0.90, 0.65, 0.03])
ax_frequency = plt.axes([0.12, 0.85, 0.65, 0.03])
ax_phase = plt.axes([0.12, 0.80, 0.65, 0.03])
ax_noise_mean = plt.axes([0.12, 0.75, 0.65, 0.03])
ax_noise_std = plt.axes([0.12, 0.70, 0.65, 0.03])
ax_sigma = plt.axes([0.12, 0.65, 0.65, 0.03])
ax_cb = plt.axes([0.84, 0.85, 0.12, 0.05])
ax_butt = plt.axes([0.84, 0.75, 0.12, 0.05])


amplitude_slider = Slider(ax_amplitude, 'Amplitude (А)', 0.0, 10.0, valinit=start_amplitude)
amplitude_slider.on_changed(update_plots)

frequency_slider = Slider(ax_frequency, 'Frequency (f)', 0.1, 10.0, valinit=start_frequency)
frequency_slider.on_changed(update_plots)

phase_slider = Slider(ax_phase, 'Phase (φ)', 0.0, 2*np.pi, valinit=start_phase)
phase_slider.on_changed(update_plots)

noise_mean_slider = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=start_noise_mean)
noise_mean_slider.on_changed(update_noise)

noise_std_slider = Slider(ax_noise_std, 'Noise Std', 0.0, 1.0, valinit=start_noise_std)
noise_std_slider.on_changed(update_noise)

gauss_sigma_slider = Slider(ax_sigma, 'Gaussian', 0.1, 10.0, valinit=start_guassian_sigma)
gauss_sigma_slider.on_changed(update_plots)

noise_butt = CheckButtons(ax_cb, ['Show Noise'], [True])
noise_butt.on_clicked(update_plots)

btn = Button(ax_butt, 'Reset', color='lightcoral')
btn.on_clicked(reset_all)


ax_raw = plt.axes([0.05, 0.36, 0.80, 0.25])
ax_filtered = plt.axes([0.05, 0.05, 0.80, 0.25])

initial_raw = generate_harmonic(time, start_amplitude, start_frequency, start_phase, noise, True)
ax_raw.grid(True)
plot_raw, = ax_raw.plot(time, initial_raw, color='#6bbb11')
ax_raw.set_title('Harmonic')


initial_filtered = apply_gaussian(initial_raw, start_guassian_sigma)
ax_filtered.grid(True)
plot_filtered, = ax_filtered.plot(time, initial_filtered, color='orange')
ax_filtered.set_title('Harmonic after Gaussian filtering')




print(
    "Інструкції для роботи з програмою:\n"
    "1. Використовуйте слайдери \"Amplitude\", \"Frequency\" та \"Phase\" для налаштування параметрів гармонічного сигналу.\n"
    "2. Налаштуйте параметри шуму за допомогою слайдерів \"Noise Mean\" (середнє) та \"Noise Std\" (стандартне відхилення).\n"
    "3. Позначте або зніміть галочку \"Show Noise\", щоб увімкнути або вимкнути додавання шуму до сигналу.\n"
    "4. Регулюйте слайдер \"Gaussian\" для зміни параметра фільтрації сигналу.\n"
    "5. Натисніть кнопку \"Reset\", щоб повернути всі налаштування до початкових значень."
)

plt.show()