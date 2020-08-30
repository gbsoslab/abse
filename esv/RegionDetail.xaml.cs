using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Windows.Threading;
using DevExpress.Xpf.Charts;
using DevExpress.Xpf.Core;


namespace EvacSim
{
    /// <summary>
    /// Interaction logic for RegionDetail.xaml
    /// </summary>
    public partial class RegionDetail : ThemedWindow
    {
        private SeriesPoint3DStorage storage;

        public string RegionInfo
        {
            get { return region_info.ToString(); }
        }
        private byte[,] region_info;

        public bool isActive { get; set; }

        public RegionDetail(byte[] init, int idx)
        {
            InitializeComponent();
            InitalizeChart(init, idx);
        }

        private void InitalizeChart(byte[] init, int idx)
        {
            isActive = true;

            byte row_num = init[idx++];
            byte col_num = init[idx++];

            region_info = new byte[row_num, col_num];

            // Create a diagram.
            Series3DStorage diagram = new Series3DStorage();

            //chart.di
            Series3D series = new Series3D();
            diagram.Series.Add(series);
            series.View = new Bar3DSeriesView();
            storage = new SeriesPoint3DStorage();


            for (int i = 0; i < row_num; i++)
            {
                for (int j = 0; j < col_num; j++)
                {
                    region_info[i, j] = init[idx];
                    storage.Points.Add(new SeriesPoint3D(j, i, init[idx++]));
                }
            }

            series.PointSource = storage;
            RegionStatus.SeriesSource = diagram;
        }

        public void update_map(byte[] init, int idx)
        {
            byte row_num = init[idx++];
            byte col_num = init[idx++];

            Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
            {
                for (int i = 0; i < row_num; i++)
                {
                    for (int j = 0; j < col_num; j++)
                    {
                        region_info[i, j] = init[idx];
                        storage.Points[col_num * i + j].Value = init[idx++];
                    }
                }
            }));
        }

        private void OnClosingHandler(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if(isActive)
                e.Cancel = true;
            this.Hide();
        }
    }
}
