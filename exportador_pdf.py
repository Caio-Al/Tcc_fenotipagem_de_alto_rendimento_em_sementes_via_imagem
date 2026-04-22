from fpdf import FPDF
import os

class ExportadorRelatorio:
    def gerar_pdf(self, lista_sementes, nome_arquivo="resultados/relatorio_fenotipagem.pdf"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Relatorio de Fenotipagem de Alto Rendimento", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", 'I', 10)
        texto_intro = ("A tabela de atributos e construida baseada em features por semente que formam uma "
                       "tabela (linhas = sementes; colunas = medidas morfologicas/cromaticas), a partir da qual se "
                       "realizam comparacoes entre lotes, deteccao de irregulares e analises de classificacao.")
        pdf.multi_cell(0, 5, txt=texto_intro)
        pdf.ln(8)
        
        unidade = lista_sementes[0].unidade if lista_sementes else "px"
        unidade_area = f"{unidade}²"
        pdf.set_font("Arial", 'B', 8)
        col_w = [10, 25, 25, 25, 25, 25, 25, 30] 
        headers = ["ID", f"Area ({unidade_area})", f"Perim. ({unidade})", f"Compr. ({unidade})", f"Larg. ({unidade})", "Circularid.", "Razao Asp.", "Cor (RGB)"]

        
        for i in range(len(headers)):
            pdf.cell(col_w[i], 8, txt=headers[i], border=1, align='C')
        pdf.ln()
        
        pdf.set_font("Arial", '', 8)
        for s in lista_sementes:
            pdf.cell(col_w[0], 6, txt=str(s.id_semente), border=1, align='C')
            pdf.cell(col_w[1], 6, txt=f"{s.area:.1f}", border=1, align='C')
            pdf.cell(col_w[2], 6, txt=f"{s.perimetro:.1f}", border=1, align='C')
            pdf.cell(col_w[3], 6, txt=f"{s.comprimento:.1f}", border=1, align='C')
            pdf.cell(col_w[4], 6, txt=f"{s.largura:.1f}", border=1, align='C')
            pdf.cell(col_w[5], 6, txt=f"{s.circularidade:.4f}", border=1, align='C')
            pdf.cell(col_w[6], 6, txt=f"{s.razao_aspecto:.4f}", border=1, align='C')
            pdf.cell(col_w[7], 6, txt=str(s.cor_rgb), border=1, align='C')
            pdf.ln()
        pdf.set_font("Arial", 'B', 8)
        pdf.ln(15)

        n = len(lista_sementes)
        if n > 0:
            media_area       = sum(s.area for s in lista_sementes) / n
            media_perim      = sum(s.perimetro for s in lista_sementes) / n
            media_compr      = sum(s.comprimento for s in lista_sementes) / n
            media_larg       = sum(s.largura for s in lista_sementes) / n
            media_circ       = sum(s.circularidade for s in lista_sementes) / n
            media_asp        = sum(s.razao_aspecto for s in lista_sementes) / n
            media_r          = sum(s.cor_rgb[0] for s in lista_sementes) / n
            media_g          = sum(s.cor_rgb[1] for s in lista_sementes) / n
            media_b          = sum(s.cor_rgb[2] for s in lista_sementes) / n

            pdf.cell(col_w[0], 6, txt="Media", border=1, align='C')
            pdf.cell(col_w[1], 6, txt=f"{media_area:.1f}", border=1, align='C')
            pdf.cell(col_w[2], 6, txt=f"{media_perim:.1f}", border=1, align='C')          
            pdf.cell(col_w[3], 6, txt=f"{media_compr:.1f}", border=1, align='C')
            pdf.cell(col_w[4], 6, txt=f"{media_larg:.1f}", border=1, align='C')
            pdf.cell(col_w[5], 6, txt=f"{media_circ:.4f}", border=1, align='C')
            pdf.cell(col_w[6], 6, txt=f"{media_asp:.4f}", border=1, align='C')
            pdf.cell(col_w[7], 6, txt=f"({int(media_r)},{int(media_g)},{int(media_b)})", border=1, align='C')
            pdf.ln()
        
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt="Analise Individual das Sementes", ln=True)
        pdf.ln(2)
        
        for s in lista_sementes:
            if pdf.get_y() > 250:
                pdf.add_page()
                
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, txt=f"Semente ID: {s.id_semente}", ln=True)
            
            pdf.set_font("Arial", '', 9)
            caminho_img = f"resultados/sementes_isoladas/semente_{s.id_semente}.png"
            
            y_atual = pdf.get_y()
            
            if os.path.exists(caminho_img):
                pdf.image(caminho_img, x=15, y=y_atual, w=15)
            
            pos_x_texto = 35
            pdf.set_xy(pos_x_texto, y_atual)
            pdf.cell(0, 5, txt=f"Area: {s.area:.2f} {unidade_area} | Perimetro: {s.perimetro:.2f} {unidade}", ln=True)
            
            pdf.set_x(pos_x_texto)
            pdf.cell(0, 5, txt=f"Comprimento: {s.comprimento:.2f} {unidade} | Largura: {s.largura:.2f} {unidade}", ln=True)
            
            pdf.set_x(pos_x_texto)
            pdf.cell(0, 5, txt=f"Circularidade: {s.circularidade:.4f} | Razao de Aspecto: {s.razao_aspecto:.4f}", ln=True)
            
            pdf.set_y(y_atual + 20)
            
            
        pdf.output(nome_arquivo)
        print(f"[Exportador] PDF gerado com sucesso em: {nome_arquivo}")