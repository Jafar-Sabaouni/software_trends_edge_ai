# Audio-to-Text Benchmark Analysis

This report summarizes the performance of a local Whisper model compared to estimated cloud performance.

### Note on Cloud Data
The 'Cloud' data presented in this report is **estimated** and derived from static, pre-computed values found in `results/cloud_results.json`. This approach was adopted because free-tier cloud transcription APIs proved unreliable for consistent benchmarking. As such, the cloud performance metrics do not reflect real-time API calls but rather serve as a theoretical benchmark based on expected performance.

### Cloud Estimation Formula
The estimation for cloud transcription time (T) is calculated using the following formula:
```
T = D * RTF + L
```
Where:
- `D` is the audio length in seconds.
- `RTF` is the Real-Time Factor. (e.g., 0.1 means 10 seconds of audio are processed in 1 second).
- `L` is extra latency, including upload time and network delays, in seconds.

#### How to get values:
- **Real-Time Factor (RTF):** Based on benchmarks from Whisper API tests and community data, Whisper Large on a GPU typically achieves an RTF around `0.1` (processing 10 seconds of audio in 1 second).
- **Latency (L):** Based on average API round-trip and upload delays reported by developers testing Whisper in cloud setups, this is typically around `1 to 3` seconds.

#### Example:
For a 120-second audio file (D = 120):
```
RTF = 0.1
L = 2 seconds (average)

T = 120 * 0.1 + 2
T = 12 + 2
T = 14 seconds
```
This estimation is not perfect but provides a good basis for planning or rough scaling estimates.

## Latency Comparison (in seconds)

| file         |   Cloud (Whisper-1) |   Local Whisper (base) |
|:-------------|--------------------:|-----------------------:|
| greeting.mp3 |                 2.7 |                1.1931  |
| nonsens.wav  |                 5   |                4.36694 |

## Full Results

| model                | file         | transcription                                                                                                                                                                                                                                                                                                                                                                                                                                                 |   duration_seconds |
|:---------------------|:-------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------:|
| Local Whisper (base) | greeting.mp3 | Hello, this is a test to test audio to text.                                                                                                                                                                                                                                                                                                                                                                                                                  |            1.1931  |
| Local Whisper (base) | nonsens.wav  | Hallo! Vandaag liepen Rosenkoelkast over straat, terwijl hij een liedje zong over bananen en wiffy-signale. Ondertussen proberen een soupkom, een sollicitatie te doen bij een fabriek die lezers maakt, maar hij wist niet hoe CV's schrijven werkt. Uiteindelijk besloot iedereen dat zwaartekracht vandaag vakantie had en dat stoelen dus mag te vliegen. Aan het einde van de dag dronk de maan een koffie en zij, wow dat was vreemd, maar wel gezellig |            4.36694 |
| Cloud (Whisper-1)    | greeting.mp3 | Hello, this is a test to test audio to text.                                                                                                                                                                                                                                                                                                                                                                                                                  |            2.7     |
| Cloud (Whisper-1)    | nonsens.wav  | Hallo! Vandaag liep Rosenkoelkast over straat, terwijl hij een liedje zong over bananen en wiffy-signale. Ondertussen proberen een soupkom, een sollicitatie te doen bij een fabriek die lezers maakt, maar hij wist niet hoe CV's schrijven werkt. Uiteindelijk besloot iedereen dat zwaartekracht vandaag vakantie had en dat stoelen dus mag te vliegen. Aan het einde van de dag dronk de maan een koffie en zij, wow dat was vreemd, maar wel gezellig   |            5       |

