# coding: utf-8


import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import tutorial as tut


def is_interactive():
    try:
        __IPYTHON__
    except NameError:
        return False
    else:
        return True


def plot_images(images, labels=None, figsize=(6, 6), fname=None):
    """ Plot some images """
    n_examples = len(images)
    dim = np.ceil(np.sqrt(n_examples))
    plt.figure(figsize=figsize)
    class_names = ['airplane','automobile','bird','cat','deer', 'dog','frog','horse','ship','truck']
    for i, img in enumerate(images):
        plt.subplot(dim, dim, i + 1)
        if img.shape[-1] == 3:
            img = img.astype(np.uint8)
            plt.imshow(img)
            if labels is not None:
                plt.suptitle(class_names[i])
        else:
            img = np.squeeze(img)
            plt.imshow(img, cmap=plt.cm.Greys)
        plt.axis('off')
    plt.tight_layout()
    plt.show()


def plot_cond_images(images):
    """ Plot some images """
    fig, sub = plt.subplots(nrows=3, ncols=10, figsize=(12, 4))
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    idx = 0
    for r, row in enumerate(sub):
        for j, col in enumerate(row):
            col.imshow(images[idx].astype(np.uint8))
            if r == 0:
                col.set_title(class_names[j])
            idx += 1
            col.axis('off')
    plt.show()


# Physics plotting

def rectangular_array(n=15):
    """ Return x,y coordinates for rectangular array with n^2 stations. """
    n0 = (n - 1) / 2
    return (np.mgrid[0:n, 0:n].astype(float) - n0)


def triangular_array(n=15, offset=True):
    """ Return x,y coordinates for triangular array with n^2 stations. """
    n0 = (n - 1) / 2
    x, y = np.mgrid[0:n, 0:n].astype(float) - n0
    if offset:  # offset coordinates
        x += 0.5 * ((y+1.) % 2)
    else:  # axial coordinates
        x += 0.5 * y
    y *= np.sin(np.pi / 3)
    return x, y


def plot_footprint(footprint, axis, label=None):
    """Plot a map *footprint* for an detector array specified by *v_stations*. """
    xd, yd = rectangular_array(n=9)
    filter = footprint != 0
    axis.scatter(xd[~filter], yd[~filter], c='grey', s=110, alpha=0.1, label="silent")
    circles = axis.scatter(xd[filter], yd[filter], c=footprint[filter], s=110, alpha=1, label="loud")
    cbar = plt.colorbar(circles, ax=axis)
    cbar.set_label('signal [a.u.]')
    axis.grid(True)
    if label != None:
        axis.text(0.95, 0.1, "Energy: %.1f EeV" % label, verticalalignment='top', horizontalalignment='right', transform=axis.transAxes, backgroundcolor='w')
    axis.set_aspect('equal')
    axis.set_xlim(-5, 5)
    axis.set_ylim(-5, 5)
    axis.set_xlabel('x [km]')
    axis.set_ylabel('y [km]')


def plot_multiple_footprints(footprint, fname=None, log_dir='.', title='', epoch='', nrows=2, ncols=2, labels=None):
    """ Plots the time and signal footprint in one figure """
    fig, sub = plt.subplots(nrows=nrows, ncols=ncols, figsize=(7, 5))
    for i in range(ncols):
        for j in range(nrows):
            idx = np.random.choice(np.arange(footprint.shape[0]))
            plot_footprint(np.squeeze(footprint[idx]), axis=sub[i, j], label=labels[idx] if labels is not None else None)
    plt.tight_layout()
    fig.subplots_adjust(left=0.02, top=0.95)
    plt.suptitle(title + ' ' + str(epoch), fontsize=12)
    plt.show()


def plot_total_signal(fake, data):
    """ histogram of #total signal values """
    fig, ax = plt.subplots(1)
    ax.hist(fake, bins=np.arange(0, 45, 1), density=True, label='fake', alpha=0.5)
    ax.hist(data, bins=np.arange(0, 45, 1), density=True, label='data', alpha=0.5)
    ax.set_xlabel('total signal')
    ax.set_ylabel('relative frequency')
    plt.legend(loc='upper right', fancybox=False)
    plt.show()


def plot_cell_number_histo(fake, data):
    """ histogram of #station values """
    fig, ax = plt.subplots(1)
    ax.hist(fake, bins=np.arange(0, 55, 1), density=True, label='fake', alpha=0.5)
    ax.hist(data, bins=np.arange(0, 55, 1), density=True, label='data', alpha=0.5)
    ax.set_xlabel('number of cells with signal')
    ax.set_ylabel('relative frequency')
    plt.legend(loc='upper right', fancybox=False)
    plt.show()


def plot_signal_map(footprint, axis, label, event=None, hex=False):
    """Plot a map *footprint* for an detector array specified by *v_stations*. """
    if hex is True:
        xd, yd = triangular_array()
    else:
        xd, yd = rectangular_array()
    filter = footprint != 0
    axis.scatter(xd[~filter], yd[~filter], c='grey', s=70, alpha=0.1, label="silent")
    axis.set_title("Layer %i" % (label+1), loc='right')
    if event is not None:
        axis.set_title('Event %i' % (event+1), loc='left')
    circles = axis.scatter(xd[filter], yd[filter], c=footprint[filter], s=80, alpha=1, label="loud", norm=matplotlib.colors.LogNorm(vmin=None, vmax=500))
    axis.set_aspect('equal')
    return circles


def plot_calo_images(images):
    fig = plt.figure(figsize=(11, 10))
    grid = matplotlib.gridspec.GridSpec(3, 1)
    for event, (image, sub_grid) in enumerate(zip(images, grid)):
        layers_grid = matplotlib.gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=sub_grid)
        for id, layer in enumerate(layers_grid):
            ax = plt.subplot(layer)
            scat = plot_signal_map(image[:, :, id], ax, label=id, event=event, hex=True)
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.85)
    cbar_ax = fig.add_axes([0.9, 0.05, 0.05, 0.9])
    cbar = fig.colorbar(scat, cax=cbar_ax)
    cbar.set_label('signal [a.u.]')
    plt.show()


def plot_average_image(image):
    fig, axis = plt.subplots(1, 3, figsize=(11, 4))
    for id, ax in enumerate(axis):
        scat = plot_signal_map(image[:, :, id], ax, label=id, hex=True)
        plt.tight_layout()
    fig.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.85)
    cbar_ax = fig.add_axes([0.9, 0.05, 0.05, 0.9])
    cbar = fig.colorbar(scat, cax=cbar_ax)
    cbar.set_label('signal [a.u.]')
    fig.suptitle("Average calorimeter images")
    plt.show()


def plot_layer_correlations(image, datatype=''):
    fig, axis = plt.subplots(1, 3, figsize=(11, 4))
    fig.suptitle(datatype)
    axis[0].hexbin(image[:, 0], image[:, 1], linewidth=0.3, mincnt=1, gridsize=50, extent=[0, 700, 0, 1300])
    axis[0].set_xlabel("Total signal layer 1")
    axis[0].set_ylabel("Total signal layer 2")
    axis[1].hexbin(image[:, 0], image[:, 2], linewidth=0.3, mincnt=1, gridsize=50, extent=[0, 700, 0, 900])
    axis[1].set_xlabel("Total signal layer 1")
    axis[1].set_ylabel("Total signal layer 3")
    axis[2].hexbin(image[:, 1], image[:, 2], linewidth=0.3, mincnt=1, gridsize=50, extent=[0, 1300, 0, 900])
    axis[2].set_xlabel("Total signal layer 2")
    axis[2].set_ylabel("Total signal layer 3")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def plot_lbn_weights(weights, name, cmap="OrRd",
        slot_names=("$b_{had}$", "$lj_{1}$", "$lj_{2}$", "$bj_{1}$", "$bj_{2}$",
        "$lep$", r"$\nu$", "$b_{lep}$"), hide_feynman=False, **fig_kwargs):
    # normalize weight tensor to a sum of 100 per row
    weights = weights / np.sum(weights, axis=0).reshape((1, weights.shape[1])) * 100

    # move the first row (bhad) to the bottom for illustrative purposes
    all_but_first_row = np.array(weights[1:])
    weights[-1] = weights[0]
    weights[:-1] = all_but_first_row

    # create the figure
    fig_kwargs.setdefault("figsize", (5, 2.7) if hide_feynman else (10, 5))
    fig_kwargs.setdefault("dpi", 120)
    fig = plt.figure(**fig_kwargs)
    ax = fig.add_subplot(1, 1 if hide_feynman else 2, 1)

    # create and style the plot
    ax.imshow(weights, cmap=cmap, vmin=0, vmax=100)
    ax.set_title("{} weights".format(name), fontdict={"fontsize": 12})

    ax.set_xlabel("LBN particle number")
    ax.set_xticks(list(range(weights.shape[1])))

    ax.set_ylabel("Input particle")
    ax.set_yticks(list(range(weights.shape[0])))
    ax.set_yticklabels(slot_names)

    # write weights into each bin
    for (i, j), val in np.ndenumerate(weights):
        ax.text(j, i, int(round(weights[i, j])), fontsize=8, ha="center", va="center", color="k")

    # lines to separate decay products of top quarks and the Higgs boson
    for height in [2.5, 4.5]:
        ax.plot((-0.5, weights.shape[1] - 0.5), (height, height), color="k", linewidth=0.5)

    # ttH feynman diagram
    if not hide_feynman:
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.axis("off")

        img_path = tut.get_file("lbn/images/feynman_ttH.png", silent=True)
        ax2.imshow(mpimg.imread(img_path))

        texts = [
            (10, "$b_{had}$"), (68, "$lj_{1}$"), (122, "$lj_{2}$"), (176, "$bj_{1}$"),
            (230, "$bj_{2}$"), (284, "$lep$"), (338, r"$\nu$"), (396, "$b_{lep}$"),
        ]
        for y, txt in texts:
            ax2.text(400, y, txt, fontdict={"color": "red"})

    # return figure and axes
    return fig, ax
