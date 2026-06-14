from keras import Model
from keras.layers import Bidirectional, Dense, Dot, Embedding, Input, LSTM, UnitNormalization


def build_encoder(vocab_size=12000, max_length=80, embedding_dim=96, lstm_units=64, output_dim=128):
    token_ids = Input(shape=(max_length,), name="token_ids")
    x = Embedding(vocab_size, embedding_dim, mask_zero=True, name="token_embedding")(token_ids)
    x = Bidirectional(LSTM(lstm_units), name="bi_lstm")(x)
    x = Dense(output_dim, activation="tanh", name="projection")(x)
    output = UnitNormalization(axis=1, name="normalized_embedding")(x)
    return Model(token_ids, output, name="bilstm_encoder")


def build_siamese_model(vocab_size=12000, max_length=80):
    encoder = build_encoder(vocab_size=vocab_size, max_length=max_length)

    question_input = Input(shape=(max_length,), name="question")
    chunk_input = Input(shape=(max_length,), name="document_chunk")

    question_vector = encoder(question_input)
    chunk_vector = encoder(chunk_input)
    similarity = Dot(axes=1, normalize=False, name="cosine_similarity")([question_vector, chunk_vector])
    output = Dense(1, activation="sigmoid", name="match_probability")(similarity)

    model = Model([question_input, chunk_input], output, name="siamese_bilstm_similarity")
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model, encoder
