import cv2
import numpy as np
import os

class ProcessadorImagem:
    def _salvar_diagnosticos(self, gray, blurred, thresh, thresh_filled, opening, sure_bg, dist_transform, sure_fg, unknown):
        pasta_diag = "resultados/diagnostico"
        os.makedirs(pasta_diag, exist_ok=True)

        cv2.imwrite(f"{pasta_diag}/1_gray.jpg", gray)
        cv2.imwrite(f"{pasta_diag}/2_blurred.jpg", blurred)
        cv2.imwrite(f"{pasta_diag}/3_thresh.jpg", thresh)
        cv2.imwrite(f"{pasta_diag}/4_thresh_filled.jpg", thresh_filled)
        cv2.imwrite(f"{pasta_diag}/5_opening.jpg", opening)
        cv2.imwrite(f"{pasta_diag}/6_sure_bg.jpg", sure_bg)

        dist_norm = cv2.normalize(dist_transform, None, 0, 255, cv2.NORM_MINMAX)
        dist_norm = dist_norm.astype(np.uint8)
        cv2.imwrite(f"{pasta_diag}/7_dist_transform.jpg", dist_norm)

        cv2.imwrite(f"{pasta_diag}/8_sure_fg.jpg", sure_fg)
        cv2.imwrite(f"{pasta_diag}/9_unknown.jpg", unknown)

    def obter_contornos(self, caminho_imagem):
        img = cv2.imread(caminho_imagem)

        if img is None:
            raise FileNotFoundError(f"Erro: Imagem não encontrada em {caminho_imagem}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh = cv2.threshold(
            blurred,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        im_floodfill = thresh.copy()
        h, w = thresh.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(im_floodfill, mask, (0, 0), 255)
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)
        thresh_filled = thresh | im_floodfill_inv

        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(
            thresh_filled,
            cv2.MORPH_OPEN,
            kernel,
            iterations=2
        )

        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(
            dist_transform,
            0.50 * dist_transform.max(),
            255,
            0
        )
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        markers = cv2.watershed(img, markers)

        contornos_separados = []
        for marker_id in np.unique(markers):
            if marker_id <= 1:
                continue

            mascara_individual = np.zeros(gray.shape, dtype="uint8")
            mascara_individual[markers == marker_id] = 255

            cnts, _ = cv2.findContours(
                mascara_individual,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                if cv2.contourArea(c) > 150:
                    contornos_separados.append(c)

        self._salvar_diagnosticos(
            gray, blurred, thresh, thresh_filled,
            opening, sure_bg, dist_transform, sure_fg, unknown
        )

        return img, gray, opening, contornos_separados