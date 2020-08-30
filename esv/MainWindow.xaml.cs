using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
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
using System.Windows.Threading;
using DevExpress.Diagram.Core;
using DevExpress.Xpf.Diagram;

namespace EvacSim
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : Window
    {
        private nsoftware.IPWorks.Udpport _udpport;
        private nsoftware.IPWorks.Ipdaemon _ipdaemon;
        private DataTable _dtSimLog;
        private DataTable _dtEventLog;
        private Dictionary<byte, DiagramShape> _regionMap;
        private Dictionary<DiagramShape, RegionDetail> _regionDataMap;

        public MainWindow()
        {
            InitializeComponent();
            InitializeNetworkComponent();
            InitializeUiComponent();
        }

        private void InitializeNetworkComponent()
        {
            /*
            _ipdaemon = new nsoftware.IPWorks.Ipdaemon();
            this._ipdaemon.OnConnected += new nsoftware.IPWorks.Ipdaemon.OnConnectedHandler(this.ipdaemon_OnConnected);
            this._ipdaemon.OnDataIn += new nsoftware.IPWorks.Ipdaemon.OnDataInHandler(this.ipdaemon_OnDataIn);
            this._ipdaemon.OnDisconnected += new nsoftware.IPWorks.Ipdaemon.OnDisconnectedHandler(this.ipdaemon_OnDisconnected);
            _ipdaemon.LocalPort = 19612;
            //ipdaemon1.InvokeThrough = this;
            _ipdaemon.Listening = true;
            */
            
            this._udpport = new nsoftware.IPWorks.Udpport();
            this._udpport.About = "";
            this._udpport.OnDataIn += new nsoftware.IPWorks.Udpport.OnDataInHandler(this.OnDataIn);

            _udpport.Active = false;
            _udpport.RemoteHost = "127.0.0.1";

            _udpport.LocalPort = 19612;
            _udpport.Active = true;

            _udpport.AcceptData = true;
            
        }

        private void ipdaemon_OnConnected(object sender, nsoftware.IPWorks.IpdaemonConnectedEventArgs e)
        {
            _ipdaemon.Connections[e.ConnectionId].EOL = "@";
        }

        private void ipdaemon_OnDisconnected(object sender, nsoftware.IPWorks.IpdaemonDisconnectedEventArgs e)
        {
        }

        /*
        private void ipdaemon_OnDataIn(object sender, nsoftware.IPWorks.IpdaemonDataInEventArgs e)
        {
            if (e.EOL)
            {
                string trimmed_data = Regex.Replace(e.Text, @"\s", "");
                string[] words = trimmed_data.Split('|');


                if (words[0] == "periodic")
                {
                    Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
                    {
                        _dtSimLog.Rows.Add(words[1], words[2], words[3]);
                        if (!_regionMap.ContainsKey(words[2]))
                        {
                            DiagramShape diagramItem = new DiagramShape();
                            diagramItem.Height = 100;
                            diagramItem.Width = 100;
                            diagramItem.Content = $"Region{words[2]}";
                            diagramItem.Shape = BasicShapes.Rectangle;
                            this.RegionDiagram.Items.Add(diagramItem);

                            _regionMap[words[2]] = diagramItem;
                            _regionDataMap[_regionMap[words[2]]] = new RegionDetail(words[3]);
                            RegionDiagram.ApplyCircularLayout();
                        }
                        else
                        {
                            _regionDataMap[_regionMap[words[2]]].update_map(words[3]);
                        }
                    }));

                }
                else if (words[0] == "eventual")
                {
                    Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
                    {
                        _dtEventLog.Rows.Add(words[1], words[2], words[3], words[4], words[5]);
                    }));
                }
            }
        }*/

        private void InitializeUiComponent()
        {
            _dtSimLog = new DataTable();
            _dtSimLog.Columns.AddRange(new DataColumn[]
            {
                new DataColumn("Sim. Time"),
                new DataColumn("Region ID"),
                new DataColumn("Region Info"),
            });
            SimulationLog.ItemsSource = _dtSimLog;

            _dtEventLog = new DataTable();
            _dtEventLog.Columns.AddRange(new DataColumn[]
            {
                new DataColumn("Sim. Time"),
                new DataColumn("Region ID"),
                new DataColumn("Event Type"),
                new DataColumn("Coordinate"),
                new DataColumn("Agent ID"),
            });
            EventLog.ItemsSource = _dtEventLog;

            _regionMap = new Dictionary<byte, DiagramShape>();
            _regionDataMap = new Dictionary<DiagramShape, RegionDetail>();
        }

        private void OnDataIn(object sender, nsoftware.IPWorks.UdpportDataInEventArgs e)
        {
            if (e.DatagramB[0] == 112)
            {
                int idx = sizeof(byte);
                double sim_time = BitConverter.ToDouble(e.DatagramB, idx);
                idx += sizeof(double);
                byte region_id = e.DatagramB[idx++];

                Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
                {
                    if (!_regionMap.ContainsKey(region_id))
                    {
                        DiagramShape diagramItem = new DiagramShape();
                        diagramItem.Height = 100;
                        diagramItem.Width = 100;
                        diagramItem.Content = $"Region{region_id}";
                        diagramItem.Shape = BasicShapes.Rectangle;
                        this.RegionDiagram.Items.Add(diagramItem);

                        _regionMap[region_id] = diagramItem;
                        _regionDataMap[_regionMap[region_id]] = new RegionDetail(e.DatagramB, idx);
                        RegionDiagram.ApplyCircularLayout();
                    }
                    else
                    {
                        _regionDataMap[_regionMap[region_id]].update_map(e.DatagramB, idx);
                    }

                    _dtSimLog.Rows.Add(sim_time, region_id, _regionDataMap[_regionMap[region_id]].RegionInfo);
                }));

            }
            else if (e.DatagramB[0] == 101)
            {
                int idx = sizeof(byte);
                double sim_time = BitConverter.ToDouble(e.DatagramB, idx);
                idx += sizeof(double);
                byte region_id = e.DatagramB[idx++];
                byte event_type = e.DatagramB[idx++];
                byte coord_x = e.DatagramB[idx++];
                byte coord_y = e.DatagramB[idx++];
                int agent_id = BitConverter.ToInt32(e.DatagramB, idx);
                idx += sizeof(int);

                Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
                {
                    _dtEventLog.Rows.Add(sim_time, region_id, event_type, $"({coord_x}, {coord_y})", agent_id);
                }));
            }
        }
        

        private void SimpleButton_Click(object sender, RoutedEventArgs e)
        {
            
            _dtSimLog.Rows.Clear();
            _dtEventLog.Rows.Clear();
            _regionMap.Clear();
            _regionDataMap.Clear();
            this.RegionDiagram.Items.Clear();
        }

        /*
         private void OnDataIn(object sender, nsoftware.IPWorks.UdpportDataInEventArgs e)
            {
                string trimmed_data = Regex.Replace(e.Datagram, @"\s", "");
                string[] words = trimmed_data.Split('|');

                if (words[0] == "periodic")
                {
                    Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
                    {
                        _dtSimLog.Rows.Add(words[1], words[2], words[3]);
                        if (!_regionMap.ContainsKey(words[2]))
                        {
                            DiagramShape diagramItem = new DiagramShape();
                            diagramItem.Height = 100;
                            diagramItem.Width = 100;
                            diagramItem.Content = $"Region{words[2]}";
                            diagramItem.Shape = BasicShapes.Rectangle;
                            this.RegionDiagram.Items.Add(diagramItem);

                            _regionMap[words[2]] = diagramItem;
                            _regionDataMap[_regionMap[words[2]]] = new RegionDetail(words[3]);
                            RegionDiagram.ApplyCircularLayout();
                        }
                        else
                        {
                            _regionDataMap[_regionMap[words[2]]].update_map(words[3]);
                        }
                    }));

                }
                else if (words[0] == "eventual")
                {
                    Dispatcher.Invoke(DispatcherPriority.Normal, new Action(delegate
                    {
                        _dtEventLog.Rows.Add(words[1], words[2], words[3], words[4], words[5]);
                    }));
                }
            }
        }
 */

        private void ShowingEditorEventHandler(object sender, DiagramShowingEditorEventArgs e)
        {
            e.Cancel = true;
            _regionDataMap[(DiagramShape)e.Item].Show();
        }

        private void OnClosingHandler(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _udpport.Active = false;
            _udpport.AcceptData = false;

            _regionMap.Clear();
            foreach(KeyValuePair<DiagramShape, RegionDetail> kv in _regionDataMap)
            {
                kv.Value.isActive = false;
                kv.Value.Close();
            }
            _regionDataMap.Clear();
        }
    }

}
