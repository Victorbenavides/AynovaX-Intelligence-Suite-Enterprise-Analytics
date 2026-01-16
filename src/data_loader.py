import pandas as pd
import streamlit as st
import os
from typing import Optional, List, Union
from streamlit.runtime.uploaded_file_manager import UploadedFile

class DataLoader:
    """
    Advanced Data Ingestion Engine.
    Handles single files, batch uploads, and automated merging of disjointed datasets.
    """

    def __init__(self, file_source: Union[str, List[UploadedFile]]):
        """
        Args:
            file_source: Can be a string path (for local demo) or a list of UploadedFiles (from Streamlit).
        """
        self.file_source = file_source

    @st.cache_data(show_spinner=False)
    def load_data(_self) -> pd.DataFrame:
        """
        Smart loader that differentiates between a local demo path and multiple uploaded files.
        Merges all inputs into a single Master DataFrame.
        """
        all_dfs = []
        
        # CASE A: Loading Local Demo File (String path)
        if isinstance(_self.file_source, str):
            if os.path.exists(_self.file_source):
                try:
                    df = _self._read_file(_self.file_source, is_path=True)
                    df['Source_File'] = os.path.basename(_self.file_source)
                    return df
                except Exception as e:
                    st.error(f"Error loading local demo: {e}")
                    return None
            else:
                st.error(f"Demo file not found at: {_self.file_source}")
                return None

        # CASE B: Batch Processing (List of UploadedFiles)
        elif isinstance(_self.file_source, list):
            valid_files = 0
            for uploaded_file in _self.file_source:
                try:
                    # Streamlit UploadedFile behaves like a file object
                    df = _self._read_file(uploaded_file, is_path=False)
                    
                    # Add Metadata for Audit (Which file did this row come from?)
                    df['Source_File'] = uploaded_file.name
                    all_dfs.append(df)
                    valid_files += 1
                except Exception as e:
                    st.warning(f"Skipped file '{uploaded_file.name}' due to error: {e}")
            
            if not all_dfs:
                return None
            
            # Merge all batches into one Data Lake
            master_df = pd.concat(all_dfs, ignore_index=True)
            return master_df

        return None

    def _read_file(self, file_obj, is_path: bool) -> pd.DataFrame:
        """Helper to read CSV or Excel based on extension."""
        
        # Determine filename for extension checking
        filename = file_obj if is_path else file_obj.name
        
        if filename.endswith('.csv'):
            return pd.read_csv(file_obj, encoding='ISO-8859-1')
        elif filename.endswith('.xlsx'):
            return pd.read_excel(file_obj, engine='openpyxl')
        else:
            raise ValueError("Unsupported format")