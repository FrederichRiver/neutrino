# LSTM 笔记

nn.LSTM



        input_size – The number of expected features in the input x
        这是输入参数的特征数量，比如常规的股票数据ochl代表了input size=4.

        hidden_size – The number of features in the hidden state h

        hidden状态可以大于input size，可以小于。

        num_layers – Number of recurrent layers. E.g., setting num_layers=2 would mean stacking two LSTMs together to form a stacked LSTM, with the second LSTM taking in outputs of the first LSTM and computing the final results. Default: 1
        层数，当LSTM层数越大，越容易出现梯度丢失。我们先从小层数开始试验。

        bias – If False, then the layer does not use bias weights b_ih and b_hh. Default: True

        batch_first – If True, then the input and output tensors are provided as (batch, seq, feature). Default: False

        dropout – If non-zero, introduces a Dropout layer on the outputs of each LSTM layer except the last layer, with dropout probability equal to dropout. Default: 0

        bidirectional – If True, becomes a bidirectional LSTM. Default: False

