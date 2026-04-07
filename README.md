تمام! إليك نسخة **جاهزة ومرتبة بالكامل بالإنجليزي** يمكنك نسخها مباشرة في ملف `README.md` ورفعها على GitHub:

---

# 📸 Image Processing Interactive App

An interactive image processing application built with **Python, Streamlit, and OpenCV**. Users can upload their own images or use a default image, and apply a variety of image processing operations easily without writing any code.

---

## ⚡ Features

1. **Color and Brightness Adjustments**

   * Convert images to grayscale.
   * Adjust brightness and contrast with sliders.
   * Apply negative effect.
   * Thresholding and Otsu’s method for image simplification.

2. **Filters**

   * Sharpen to enhance details.
   * Edge detection filter.
   * Blur with Gaussian Blur, including kernel size control.

3. **Edge Detection**

   * Sobel (horizontal & vertical edges).
   * Laplacian (overall edge detection).
   * Canny (fine edge detection) with adjustable thresholds.

4. **Noise Handling (Denoising)**

   * Add synthetic noise: Salt & Pepper or Gaussian.
   * Median Filter for reducing spot noise.
   * Bilateral Filter to remove noise while preserving edges.

5. **Morphological Operations**

   * Erosion to shrink objects.
   * Dilation to expand objects.
   * Opening to remove small noise.
   * Closing to fill gaps.
   * Adjustable kernel size for all operations.

6. **Geometric Transformations**

   * Translation (move image horizontally/vertically).
   * Rotation around image center.
   * Scaling (resize image).
   * Flipping (horizontal & vertical).
   * Cropping to extract a specific region.

7. **Interactive Experience**

   * All operations are interactive via menus, buttons, and sliders.
   * Save images after each modification directly.

---

## 🛠️ Requirements

* Python >= 3.9
* Required Python libraries:

```bash
pip install streamlit opencv-python pillow numpy
```

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/username/image-processing-app.git
cd image-processing-app
```

2. Run the application:

```bash
streamlit run app.py
```

3. Upload an image or use the default image to explore all interactive operations.

---

## 📁 Project Structure

```text
image-processing-app/
│
├── app.py                # Main Streamlit app file
├── default_image.jpg     # Default image for demonstration
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

---

## 💡 Notes

* Processed images can be saved directly in PNG format.
* Clear images produce the best results for filters and edge detection.
* The project can be extended with additional filters or geometric operations.

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).
