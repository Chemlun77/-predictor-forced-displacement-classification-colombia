"""
Final Report Generator for Forced Displacement Classification Models
Creates comprehensive comparison tables and visualizations for all trained models
Based on 004_figures.py style
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
from sklearn.metrics import auc
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# APA STYLE CONFIGURATION (from 004_figures.py)
# ============================================================================

FONT_SIZE_LABELS = 30
FONT_SIZE_TICKS = 28
FONT_SIZE_TITLE = 34
FONT_SIZE_ANNOTATIONS = 24
FONT_SIZE_LEGEND = 24
FONT_SIZE_SMALL = 20
DPI_SETTING = 300

# Color palette
COLOR_PRIMARY = '#3498DB'
COLOR_SECONDARY = '#E74C3C'
COLOR_TERTIARY = '#2ECC71'
COLOR_QUATERNARY = '#F39C12'
COLOR_PURPLE = '#9B59B6'
COLOR_TEAL = '#1ABC9C'
COLOR_ORANGE = '#E67E22'
COLOR_GRAY = '#95A5A6'

COLORS = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY, COLOR_QUATERNARY, 
          COLOR_PURPLE, COLOR_TEAL, COLOR_ORANGE, COLOR_GRAY]

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = FONT_SIZE_TICKS
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['figure.dpi'] = DPI_SETTING

def apply_apa_style(ax):
    """Apply APA style to axes"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

# Define paths (relative to project root)
PROJECT_ROOT = Path.cwd()
CLASSICAL_METRICS = PROJECT_ROOT / "00_predictive_displacement_model/db/02a_classical_models/metrics/all_architectures_tested_comprehensive.xlsx"
NEURAL_METRICS = PROJECT_ROOT / "00_predictive_displacement_model/db/02b_neural_networks/metrics/all_architectures_tested_comprehensive.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "00_predictive_displacement_model/fig/final_report"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. LOAD BEST MODELS METRICS
# ============================================================================

def load_best_models():
    """Load metrics for best models from both classical and neural networks"""
    
    # Load all architectures
    df_classical = pd.read_excel(CLASSICAL_METRICS)
    df_neural = pd.read_excel(NEURAL_METRICS)
    
    # Filter for best models
    best_classical_names = ['Logistic_Regression', 'Random_Forest', 'XGBoost']
    best_neural_names = ['ResNet_Style', 'Deep']
    
    # Get best architecture for each model
    best_models = []
    for model_name in best_classical_names:
        model_data = df_classical[df_classical['Model'].str.contains(model_name, na=False)]
        if not model_data.empty:
            best_arch = model_data.loc[model_data['Test_F1'].idxmax()]
            best_models.append(best_arch)
    
    for model_name in best_neural_names:
        model_data = df_neural[df_neural['Model'].str.contains(model_name, na=False)]
        if not model_data.empty:
            best_arch = model_data.loc[model_data['Test_F1'].idxmax()]
            best_models.append(best_arch)
    
    df_best = pd.DataFrame(best_models)
    return df_best

# ============================================================================
# 2. CREATE METRICS COMPARISON TABLE
# ============================================================================

def create_metrics_table(df_best):
    """Create comprehensive metrics comparison table"""
    
    table_data = []
    
    for idx, row in df_best.iterrows():
        model_name = row['Model'].split('_')[0] if '_' in row['Model'] else row['Model']
        
        table_data.append({
            'Model': model_name,
            'Training Time (min)': f"{row['Training_Time_Minutes']:.2f}",
            'Accuracy Train': f"{row['Train_Accuracy']:.4f}",
            'Precision Train': f"{row['Train_Precision']:.4f}",
            'Recall Train': f"{row['Train_Recall']:.4f}",
            'F1-Score Train': f"{row['Train_F1']:.4f}",
            'Accuracy Test': f"{row['Test_Accuracy']:.4f}",
            'Precision Test': f"{row['Test_Precision']:.4f}",
            'Recall Test': f"{row['Test_Recall']:.4f}",
            'F1-Score Test': f"{row['Test_F1']:.4f}",
            'ROC-AUC Test': f"{row['Test_ROC_AUC']:.4f}"
        })
    
    df_table = pd.DataFrame(table_data)
    
    # Save to CSV
    df_table.to_csv(OUTPUT_DIR / 'metrics_comparison_table.csv', index=False)
    
    # Print formatted table
    print("\n" + "="*120)
    print("METRICS COMPARISON TABLE - BEST MODELS")
    print("="*120)
    print(df_table.to_string(index=False))
    print("="*120 + "\n")
    
    return df_table

# ============================================================================
# 3. CREATE BAR CHART COMPARISON
# ============================================================================

def create_bar_comparison(df_best):
    """Create grouped bar chart comparing test metrics across models"""
    
    models = []
    metrics_data = {
        'Accuracy': [],
        'Precision': [],
        'Recall': [],
        'F1-Score': [],
        'ROC-AUC': []
    }
    
    for idx, row in df_best.iterrows():
        model_name = row['Model'].split('_')[0] if '_' in row['Model'] else row['Model']
        models.append(model_name)
        metrics_data['Accuracy'].append(row['Test_Accuracy'])
        metrics_data['Precision'].append(row['Test_Precision'])
        metrics_data['Recall'].append(row['Test_Recall'])
        metrics_data['F1-Score'].append(row['Test_F1'])
        metrics_data['ROC-AUC'].append(row['Test_ROC_AUC'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))
    
    x = np.arange(len(models))
    width = 0.15
    multiplier = 0
    
    for (metric_name, metric_values), color in zip(metrics_data.items(), COLORS[:5]):
        offset = width * multiplier
        rects = ax.bar(x + offset, metric_values, width, label=metric_name, color=color, 
                      edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., height + 0.01,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=FONT_SIZE_SMALL, fontweight='bold')
        
        multiplier += 1
    
    # Formatting
    ax.set_xlabel('Model', fontsize=FONT_SIZE_LABELS, fontweight='bold')
    ax.set_ylabel('Score', fontsize=FONT_SIZE_LABELS, fontweight='bold')
    ax.set_title('Test Metrics Comparison Across Models', fontsize=FONT_SIZE_TITLE, fontweight='bold', pad=20)
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(models, fontsize=FONT_SIZE_TICKS)
    ax.legend(loc='lower right', fontsize=FONT_SIZE_LEGEND)
    ax.set_ylim([0.5, 1.05])
    
    apply_apa_style(ax)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'metrics_bar_comparison.png', dpi=DPI_SETTING, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: metrics_bar_comparison.png")

# ============================================================================
# 4. CREATE INDIVIDUAL CONFUSION MATRICES
# ============================================================================

def create_confusion_matrices(df_best):
    """Create individual confusion matrix for each model (based on 004_figures.py)"""
    
    for idx, row in df_best.iterrows():
        model_name = row['Model']
        
        # Determine folder based on model type
        if model_name in ['Logistic_Regression', 'Random_Forest', 'XGBoost']:
            cm_file = PROJECT_ROOT / f"00_predictive_displacement_model/db/02a_classical_models/model_data/confusion_matrices/{model_name}_best_confusion_matrix.xlsx"
        else:
            cm_file = PROJECT_ROOT / f"00_predictive_displacement_model/db/02b_neural_networks/model_data/confusion_matrices/{model_name}_best_confusion_matrix.xlsx"
        
        if not cm_file.exists():
            print(f"  ⚠ Confusion matrix not found for {model_name}")
            continue
            
        # Load confusion matrix
        cm_df = pd.read_excel(cm_file, index_col=0)
        cm = cm_df.values
        
        # Normalize
        cm_normalized = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-15)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        im = ax.imshow(cm_normalized, cmap='Blues', aspect='auto', vmin=0, vmax=1)
        
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Others (0)', 'Displacement (1)'], fontsize=FONT_SIZE_TITLE)
        ax.set_yticklabels(['Others (0)', 'Displacement (1)'], fontsize=FONT_SIZE_TITLE, rotation=90, va='center')
        
        ax.set_ylabel('True Label', fontsize=FONT_SIZE_TITLE, fontweight='bold')
        ax.set_xlabel('Predicted Label', fontsize=FONT_SIZE_TITLE, fontweight='bold')
        # ax.set_title(f'Confusion Matrix - {model_name}', fontsize=FONT_SIZE_TITLE, fontweight='bold', pad=20)
        
        # Annotations with values and percentages
        for i in range(2):
            for j in range(2):
                proportion = cm_normalized[i, j] * 100
                text_label = f'{cm[i, j]:,}\n({proportion:.1f}%)'
                
                if (i == 0 and j == 0) or (i == 1 and j == 1):
                    color = "white"
                else:
                    color = "black"
                    
                ax.text(j, i, text_label, ha="center", va="center", 
                       color=color, fontsize=FONT_SIZE_TITLE, fontweight='bold')
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Proportion', fontsize=FONT_SIZE_TITLE, fontweight='bold')
        cbar.ax.tick_params(labelsize=FONT_SIZE_TITLE)
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f'confusion_matrix_{model_name}.png', dpi=DPI_SETTING, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Confusion matrix saved: {model_name}")

# ============================================================================
# 5. CREATE COMBINED ROC CURVE
# ============================================================================

def create_combined_roc_curve(df_best):
    """Create combined ROC curve for all models (based on 004_figures.py)"""
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    roc_data = []
    
    for idx, row in df_best.iterrows():
        model_name = row['Model']
        
        # Determine folder based on model type
        if model_name in ['Logistic_Regression', 'Random_Forest', 'XGBoost']:
            roc_file = PROJECT_ROOT / f"00_predictive_displacement_model/db/02a_classical_models/model_data/roc_data/{model_name}_best_roc_curve.xlsx"
        else:
            roc_file = PROJECT_ROOT / f"00_predictive_displacement_model/db/02b_neural_networks/model_data/roc_data/{model_name}_best_roc_curve.xlsx"
        
        if not roc_file.exists():
            print(f"  ⚠ ROC data not found for {model_name}")
            continue
            
        # Load ROC data
        roc_df = pd.read_excel(roc_file)
        fpr = roc_df['FPR'].values
        tpr = roc_df['TPR'].values
        roc_auc = roc_df['AUC'].values[0]
        
        # Plot
        display_name = model_name.replace('_', ' ')
        ax.plot(fpr, tpr, color=COLORS[idx % len(COLORS)], lw=3, 
                label=f'{display_name} (AUC = {roc_auc:.4f})')
        
        roc_data.append({
            'model': model_name,
            'auc': roc_auc,
            'fpr': fpr,
            'tpr': tpr
        })
        
        print(f"  ✓ ROC curve loaded: {model_name} (AUC = {roc_auc:.4f})")
    
    # Diagonal line
    ax.plot([0, 1], [0, 1], color=COLOR_SECONDARY, lw=2, linestyle='--', 
            label='Random Classifier (AUC = 0.5000)')
    
    # Formatting
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=FONT_SIZE_LABELS, fontweight='bold')
    ax.set_ylabel('True Positive Rate', fontsize=FONT_SIZE_LABELS, fontweight='bold')
    ax.set_title('ROC Curves - All Models', fontsize=FONT_SIZE_TITLE, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=FONT_SIZE_LEGEND)
    
    apply_apa_style(ax)
    ax.grid(alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'roc_curves_combined.png', dpi=DPI_SETTING, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Saved: roc_curves_combined.png")

# ============================================================================
# 6. CREATE FEATURE IMPORTANCE PLOT
# ============================================================================

def create_feature_importance():
    """Create feature importance plot for Random Forest (based on 004_figures.py)"""
    
    # Load Random Forest model
    model_path = PROJECT_ROOT / "00_predictive_displacement_model/db/02a_classical_models/saved_models/Random_Forest_best_model.pkl"
    
    if not model_path.exists():
        print("  ⚠ Random Forest model not found")
        return
    
    model = joblib.load(model_path)
    print(f"✓ Model loaded: {model.n_features_in_} features")
    
    # Extract importances
    importances = model.feature_importances_
    importances_pct = (importances / importances.sum()) * 100
    
    # Load feature names
    feature_names_path = PROJECT_ROOT / "00_predictive_displacement_model/db/02a_classical_models/model_data/feature_names.xlsx"
    if feature_names_path.exists():
        feature_names_df = pd.read_excel(feature_names_path)
        feature_names = feature_names_df['Feature_Name'].tolist()
    else:
        # Generic names if file doesn't exist
        feature_names = [f'Feature_{i+1}' for i in range(len(importances))]
    
    # Create DataFrame
    df_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance_%': importances_pct
    }).sort_values('Importance_%', ascending=False).reset_index(drop=True)
    
    print(f"\nTop 10 most important features:")
    print(df_importance.head(10))
    
    # Plot top 20 (reversed for proper display)
    df_plot = df_importance.head(20).iloc[::-1]
    
    fig, ax = plt.subplots(figsize=(14, max(10, len(df_plot) * 0.5)))
    
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(df_plot)))
    
    bars = ax.barh(range(len(df_plot)), df_plot['Importance_%'],
                   color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_yticks(range(len(df_plot)))
    ax.set_yticklabels(df_plot['Feature'], fontsize=FONT_SIZE_TICKS)
    ax.set_xlabel('Importance (%)', fontsize=FONT_SIZE_LABELS, fontweight='bold')
    # ax.set_title('Top 20 Features - Random Forest Importance', 
    #              fontsize=FONT_SIZE_TITLE, fontweight='bold', pad=20)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, df_plot['Importance_%'])):
        ax.text(val + 0.5, i, f'{val:.1f}%', va='center', 
                fontsize=FONT_SIZE_ANNOTATIONS - 4, fontweight='bold')
    
    apply_apa_style(ax)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'feature_importance.png', dpi=DPI_SETTING, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Saved: feature_importance.png")
    
    # Save table
    df_importance['Rank'] = range(1, len(df_importance) + 1)
    df_table = df_importance[['Rank', 'Feature', 'Importance_%']]
    df_table.to_excel(OUTPUT_DIR / 'feature_importance_table.xlsx', index=False)
    print(f"✓ Saved: feature_importance_table.xlsx")

# ============================================================================
# 7. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("GENERATING FINAL REPORT")
    print("="*80 + "\n")
    
    # Load best models
    print("📊 Loading best models metrics...")
    df_best = load_best_models()
    print(f"   Loaded {len(df_best)} models\n")
    
    # Create metrics table
    print("📋 Creating metrics comparison table...")
    df_table = create_metrics_table(df_best)
    
    # Create bar comparison
    print("\n📊 Creating bar chart comparison...")
    create_bar_comparison(df_best)
    
    # Create confusion matrices
    print("\n📊 Creating confusion matrices...")
    create_confusion_matrices(df_best)
    
    # Create ROC curves
    print("\n📊 Creating ROC curves...")
    create_combined_roc_curve(df_best)
    
    # Create feature importance
    print("\n📊 Creating feature importance plot...")
    create_feature_importance()
    
    print("\n" + "="*80)
    print(f"✅ REPORT GENERATION COMPLETE")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()