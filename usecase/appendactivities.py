import streamlit as st
import pandas as pd
import io
from helpers.io import readExcel, validateColumns, produceExcel

PRIMARY_COLUMNS = ["activity_time", "project_name", "task_id", "status", "assigned_to"]
exampleData = [{
    "id_tms": 1,
    "period": "2026-11",
    "availability": 100,
    "issue_key": "PROJ-123",
    "issue_id": 12345,
    "project_key": "PROJ",
    "activity": "Development",
    "status": "Done",
    "priority": "High",
    "activity_time": "2026-11-04 09:00:00",
    "timespent": 3600,
    "status_taiga": "Closed",
    "project_name": "Project A",
    "created_task": "2026-11-01 08:00:00",
    "modified_task": "2026-11-04 09:00:00",
    "story": "test story",
    "creaated_story": "2026-11-01 08:00:00",
    "modified_story": "2026-11-03 10:00:00",
    "finished_story": "2026-11-04 09:00:00",
    "epic": "test epic",
    "creaated_epic": "2026-10-01 08:00:00",
    "modified_epic": "2026-11-01 10:00:00"
}]
expectedColumn = list(exampleData[0].keys())
def auth(secretKeyInput, secretKeyExpected):
    return secretKeyInput == secretKeyExpected

def masterTemplate():
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        pd.DataFrame(exampleData).to_excel(writer, index=False)
    return buffer.getvalue()

def appendActivities():
    for key, default in {
        "master_df": None,
        "incremental_df": None,
        "result_df": None,
        "result_bytes": None,
        "master_name": None,
        "incremental_name": None,
        "master_last_datetime": None, 
        "incremental_last_datetime": None,
        "is_execute": None,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    st.title("Tambah & Sinkronisasi Aktivitas")
    st.markdown(
        '<p class="subtitle">Kelola data master aktivitas dan gabungkan data berkala untuk pelaporan sprint Taiga.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
        <div class="section-heading"><span class="section-number">1</span> Data Master Aktivitas <span class="tag">MASTER_BASELINE</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Unggah file master aktivitas (.xlsx)"):
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<div class="inner-card">', unsafe_allow_html=True)
            st.markdown('<div class="inner-title">📄 Unduh Template Master</div>', unsafe_allow_html=True)
            st.markdown('<div class="inner-card">', unsafe_allow_html=True)
            st.download_button(
                        "Download Template",
                        data=masterTemplate(),
                        file_name="template_aktivitas.xlsx",
                        use_container_width=True,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        
        with col2:
            st.markdown('<div class="inner-card">', unsafe_allow_html=True)
            st.markdown('<div class="inner-title">☁️ Upload Data Master</div>', unsafe_allow_html=True)
            masterData = st.file_uploader(
                "Pilih file master (.xlsx)",
                type=["xlsx"],
                key="master_uploader",
                help=f"File Excel harus memiliki kolom: {', '.join(expectedColumn)}",
            )
            if masterData is not None:
                excelFile = pd.ExcelFile(masterData)
                sheetNames = excelFile.sheet_names
                selectedSheet = st.selectbox(
                    "Pilih Sheet Master",
                    index=None,
                    options=sheetNames,
                    help="Pilih worksheet yang berisi data master."
                )
                if selectedSheet:
                    try:
                        dfMaster = readExcel(masterData, 
                                            sheetName=selectedSheet,
                                            parseDates=["activity_time"]).sort_values(by="activity_time", ascending=True).reset_index(drop=True)
                        errors = validateColumns(dfMaster, "Data Master", expectedColumn)
                        if errors: 
                            st.error("\n".join(errors))
                            st.session_state.master_df = None
                            st.stop()

                        st.write("Preview Data Master")
                        st.write(dfMaster.head())
                        st.session_state.master_df = dfMaster
                        st.session_state.master_name = masterData.name
                        st.session_state.master_last_datetime = dfMaster.iloc[-1]["activity_time"]
                        st.success(f"File terbaca: {st.session_state.master_name} · {len(dfMaster):,} baris.")
                    except Exception as exc:
                        st.error(f"Gagal membaca file master: {exc}")
                        st.session_state.master_df = None
            elif st.session_state.master_df is not None:
                st.caption(
                    f"File aktif: {st.session_state.master_name} · "
                    f"{len(st.session_state.master_df):,} baris"
                )

    st.markdown(
        """
        <div class="section-card">
        <div class="section-heading"><span class="section-number">2</span> Data Aktivitas Tambahan (Incremental) <span class="tag" style="background:#fcebed;color:#b81120">DELTA</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Unggah file increment aktivitas (.xlsx)"):
        incrementalData = st.file_uploader(
            "File Data Tambahan (Excel .xlsx)",
            type=["xlsx"],
            key="incremental_uploader",
            help=f"File Excel harus memiliki kolom: {', '.join(expectedColumn)}",
        )
        
        if incrementalData is not None:
            excelFile = pd.ExcelFile(incrementalData)
            sheetNames = excelFile.sheet_names
            selectedSheet = st.selectbox(
                "Pilih Sheet Data Tambahan",
                options=sheetNames,
                index=None,
                help="Pilih worksheet yang berisi data tambahan."
            )
            if selectedSheet:
                try:
                    dfIncrement = readExcel(incrementalData, sheetName=selectedSheet,
                                            parseDates=["activity_time"]).sort_values(by="activity_time", ascending=True).reset_index(drop=True)
                    errors = validateColumns(dfIncrement, "Data Tambahan", expectedColumn)
                    if errors: 
                        st.error("\n".join(errors))
                        st.session_state.incremental_df = None
                        st.stop()

                    st.write("Preview Data Tambahan")
                    st.write(dfIncrement.head())
                    st.session_state.incremental_df = dfIncrement
                    st.session_state.incremental_name = incrementalData.name
                    st.session_state.incremental_last_datetime = dfIncrement.iloc[-1]["activity_time"]
                    st.success(f"File terbaca: {st.session_state.incremental_name} · {len(dfIncrement):,} baris.")
                except Exception as exc:
                    st.error(f"Gagal membaca file tambahan: {exc}")
                    st.session_state.incremental_df = None
        elif st.session_state.incremental_df is not None:
            st.caption(
                f"File aktif: {st.session_state.incremental_name} · "
                f"{len(st.session_state.incremental_df):,} baris"
            )

    st.markdown(
        """
        <div class="section-card">
        <div class="section-heading"><span class="section-number">3</span> Proses Konfigurasi <span class="tag" style="background:#fcebed;color:#b81120">PROCESS</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Mulai Konfigurasi Eksekusi"):
        date1, date2 = st.columns(2, gap="medium")
        with date1:
            lastDateMaster = st.datetime_input(
                "Batas Akhir Data Master (Last Date)",
                value=st.session_state.master_last_datetime,
                help="Baris pada data tambahan dengan activity_time lebih awal dari nilai ini tidak akan digabungkan.",
            )
            if lastDateMaster is not None:
                st.session_state.master_last_datetime = lastDateMaster
                st.caption(f"`start_date_data_tambahan > {lastDateMaster.strftime('%Y-%m-%d')}`")
        with date2:
            lastDateDelta = st.datetime_input(
                "Batas Akhir Data Tambahan (Last Date)",
                value=st.session_state.incremental_last_datetime,
                help="Baris pada data tambahan dengan activity_time lebih dari nilai ini tidak akan digabungkan.",
            )
            if lastDateDelta is not None:
                st.session_state.incremental_last_datetime = lastDateDelta
                st.caption(f"`end_date_data_tambahan <= {lastDateDelta.strftime('%Y-%m-%d')}`")

        st.markdown(
            """
            <div class="info-callout">
            <strong>ⓘ Logika Sinkronisasi Data Concat</strong><br>
            Hanya baris data tambahan dengan <code>activity_time <= Last Date</code>
            dan berada di atas last date data master yang dipilih yang akan ditautkan ke data
            output.
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    if (lastDateMaster is not None) and (lastDateDelta is not None) and (lastDateDelta < lastDateMaster):
        st.warning("cut off data tambahan tidak boleh kurang dari cut off data master")
        st.stop()

    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.master_df is None or st.session_state.incremental_df is None:
        st.warning("belum siap untuk exec")
        st.stop()

    if st.button(
        "Execute",
        use_container_width=True,
    ) or st.session_state.is_execute == True:
        st.session_state.is_execute = True
        dfMaster = st.session_state.master_df[st.session_state.master_df["activity_time"] <= lastDateMaster].copy()
        dfIncrement = st.session_state.incremental_df[
            (st.session_state.incremental_df["activity_time"] > lastDateMaster) &
            (st.session_state.incremental_df["activity_time"] <= lastDateDelta)].copy()

        df = pd.concat([dfMaster, dfIncrement], ignore_index=True, sort=False)
        dfCols = df.columns

        with st.expander("Pilih Kolom Tertentu ?"):
            colOpt = st.multiselect("Kolom Output", dfCols, default=dfCols)
            df = df[colOpt]

        df = df.sort_values(by='activity_time', ascending=True)

        st.download_button(
            "Download Final Data",
            data=produceExcel(df, "final_activities"),
            file_name="final_activities.xlsx",
            use_container_width=True,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
       
    st.divider()
    st.markdown(
        """
        <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;
                    color:#7b818b;font: .72rem 'JetBrains Mono',monospace;padding:4px 2px;">
        <span>Management Taiga</span>
        </div>
        """,
        unsafe_allow_html=True,
    )