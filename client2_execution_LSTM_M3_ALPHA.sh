#!/bin/bash
#LSTM



alphas="0.001 0.01 0.1 0.02 0.2 0.005 0.05 0.5 0.075 1.0 1000000.0"

for var in $alphas; do
  echo $var
  #HERE GOES THE WHOLE SEQUENCE:



#FOR SEQ80
#_FedAvg
sleep 500
python3 fl_testbed/version2/client/federated_client_RUL_FedAvg.py   -cn 1 -cm 5 -e 1 -dfn   'M3_5_1_ddf_LSTM.pkl' -dfn_test_x   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_inputs.pkl' -dfn_test_y   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_out.pkl'   -ip 172.17.0.4 2>&1 | tee LSTM_CLIENT2_FedAvg_${var}.txt
#_FedAvgM
sleep 300
python3 fl_testbed/version2/client/federated_client_RUL_FedAvgM.py   -cn 1 -cm 5 -e 1 -dfn   'M3_5_1_ddf_LSTM.pkl' -dfn_test_x   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_inputs.pkl' -dfn_test_y   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_out.pkl'   -ip 172.17.0.4 2>&1 | tee LSTM_CLIENT2_FedAvgM_${var}.txt
#_FedOpt
sleep 300
python3 fl_testbed/version2/client/federated_client_RUL_FedOpt.py   -cn 1 -cm 5 -e 1 -dfn   'M3_5_1_ddf_LSTM.pkl' -dfn_test_x   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_inputs.pkl' -dfn_test_y   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_out.pkl'   -ip 172.17.0.4 2>&1 | tee LSTM_CLIENT2_FedOpt_${var}.txt
#_QFedAvg
sleep 300
python3 fl_testbed/version2/client/federated_client_RUL_QFedAvg.py   -cn 1 -cm 5 -e 1 -dfn   'M3_5_1_ddf_LSTM.pkl' -dfn_test_x   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_inputs.pkl' -dfn_test_y   '100_2_15_15_combined_offset_misalignment_M3.csv__client_centralizedtest_out.pkl'   -ip 172.17.0.4 2>&1 | tee LSTM_CLIENT2_QFedAvg_${var}.txt



  echo "done"
done