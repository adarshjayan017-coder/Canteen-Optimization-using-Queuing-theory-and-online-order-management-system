import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime, timedelta
from core.db_config import get_db_connection

def get_mrp_forecast():
    """
    Authentic MRP engine: Validates accuracy and sets specific target dates.
    """
    conn = get_db_connection()
    try:
        # Step 1: Query actual sales data
        query = """
            SELECT DATE(o.created_at) as ds, m.item_name, SUM(oi.quantity) as y
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu m ON oi.item_id = m.item_id
            WHERE o.status = 'completed'
            GROUP BY ds, m.item_name
            ORDER BY ds ASC
        """
        df = pd.read_sql(query, conn)
        df['ds'] = pd.to_datetime(df['ds'])

        # Step 2: Determine 'Next Working Day'
        target_date = datetime.now() + timedelta(days=1)
        while target_date.weekday() >= 5:  # Skip Sat (5) and Sun (6)
            target_date += timedelta(days=1)

        production_plan = []
        
        for item in df['item_name'].unique():
            item_df = df[df['item_name'] == item][['ds', 'y']]
            if len(item_df) < 10: continue 

            # Step 3: Reliability Calculation (Backtesting)
            train, test = item_df.iloc[:-3], item_df.iloc[-3:]
            model_test = Prophet(yearly_seasonality=False, daily_seasonality=True)
            model_test.fit(train)
            
            test_forecast = model_test.predict(test[['ds']])
            # Fix negative accuracy: use MAPE and cap at 0
            mape = np.mean(np.abs((test['y'].values - test_forecast['yhat'].values) / test['y'].values)) * 100
            reliability = max(0, round(100 - mape, 1))
            
            # Step 4: Final Forecast with Weekday Mask
            final_model = Prophet(yearly_seasonality=False, daily_seasonality=True)
            final_model.fit(item_df)
            future = final_model.make_future_dataframe(periods=10)
            future = future[future['ds'].dt.weekday < 5] # Remove weekends
            
            forecast = final_model.predict(future)
            
            # Get prediction for specific target_date
            target_pred = forecast[forecast['ds'] == pd.to_datetime(target_date.date())]
            qty = round(target_pred.iloc[0]['yhat']) if not target_pred.empty else 0

            production_plan.append({
                'name': item,
                'target_date_str': target_date.strftime('%A, %d %b %Y'),
                'tomorrow_qty': qty,
                'accuracy': reliability,
                'forecast_data': forecast[forecast['ds'] > df['ds'].max()].head(5).to_dict(orient='records'),
                'history_data': item_df.tail(7).to_dict(orient='records')
            })

        return production_plan, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()