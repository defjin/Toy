using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Speech.Recognition;
using Microsoft.Speech.Synthesis;

namespace 음성인식
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {
        bool isWorking = true;

        public MainWindow()
        {
            InitializeComponent();
            Init();            
        }

        public void Init()
        {
        }

        public void recognizer_SpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {
            label1.Content = "Recognized text: " + e.Result.Text;
        }

        private void endButton_Click(object sender, RoutedEventArgs e)
        {
            isWorking = false;
        }

        private void startButton_Click(object sender, RoutedEventArgs e)
        {
            using (SpeechRecognitionEngine recognizer = new SpeechRecognitionEngine())
            {
                Grammar grammar = new Grammar("RecogGrammer.xml");
                recognizer.LoadGrammarAsync(grammar);

                recognizer.SetInputToDefaultAudioDevice();


                recognizer.SpeechRecognized += new EventHandler<SpeechRecognizedEventArgs>(recognizer_SpeechRecognized);

                recognizer.RecognizeAsync(RecognizeMode.Multiple);

                while (isWorking == true)
                {

                }
            }
        }
    }
}
