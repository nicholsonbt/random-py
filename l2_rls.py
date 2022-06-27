import numpy as np

def train(data, labels):
    # Add a column of zeros to the left of the data.
    X_tilde = np.append(np.zeros((data.shape[0], 1)), data, axis=1)

    # Calculate the Moore-Penrose Inverse.
    mpi = np.linalg.pinv(X_tilde)

    # Calculate the coefficients for the given data and labels.
    w = np.dot(mpi, labels)

    # Return the coefficients.
    return w

def predict(w, data):
    # Add a column of zeros to the left of the data.
    phi = np.append(np.zeros((data.shape[0], 1)), data, axis=1)

    # Predict the labels for the data using the coefficients and data given.
    y_hat = np.dot(phi, w)

    # Return the predicted labels.
    return y_hat

